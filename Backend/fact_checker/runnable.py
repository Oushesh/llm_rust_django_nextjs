#from typing import Generator, Union, Other, Callable, Any, List
from abc import ABC
from serializable import Serializable
from config import ensure_config, get_executor_for_config, patch_config, RunnableConfig

import asyncio
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    TypeVar,
    Union,
    cast,
)

Input = TypeVar("Input")
# Output type should implement __concat__, as eg str, list, dict do
Output = TypeVar("Output")
Other = TypeVar("Other")



class Runnable(Generic[Input,Output],ABC):
    """A Runnable is a unit of work that can be invoked, batched, streamed, or
    transformed."""
    def __or__(
        self,
        other,
    ):
        #pass
        return RunnableSequence(first=self, last=coerce_to_runnable(other))

    def __ror__(
        self,
        other,
    ):
        pass
        #return RunnableSequence(first=coerce_to_runnable(other), last=self)


    def batch(
        self,
        inputs,
        config,
        **kwargs,
    ):
        """
        Default implementation of batch, which calls invoke N times.
        Subclasses should override this method if they can batch more efficiently.
        """
        configs = self._get_config_list(config, len(inputs))

        # If there's only one input, don't bother with the executor
        if len(inputs) == 1:
            return [self.invoke(inputs[0], configs[0], **kwargs)]

        with get_executor_for_config(configs[0]) as executor:
            return list(executor.map(partial(self.invoke, **kwargs), inputs, configs))

    async def abatch(
        self,
        inputs,
        config,
        **kwargs,
    ):
        """
        Default implementation of abatch, which calls ainvoke N times.
        Subclasses should override this method if they can batch more efficiently.
        """
        configs = self._get_config_list(config, len(inputs))
        coros = map(partial(self.ainvoke, **kwargs), inputs, configs)

        return await gather_with_concurrency(configs[0].get("max_concurrency"), *coros)

    def stream(
        self,
        input,
        config,
        **kwargs,
    ):
        """
        Default implementation of stream, which calls invoke.
        Subclasses should override this method if they support streaming output.
        """
        yield self.invoke(input, config, **kwargs)


    def transform(
        self,
        input,
        config,
        **kwargs,
    ):
        """
        Default implementation of transform, which buffers input and then calls stream.
        Subclasses should override this method if they can start producing output while
        input is still being generated.
        """

        for chunk in input:
            if final is None:
                final = chunk
            else:
                # Make a best effort to gather, for any type that supports `+`
                # This method should throw an error if gathering fails.
                final += chunk  # type: ignore[operator]
        if final:
            yield from self.stream(final, config, **kwargs)


    def bind(self, **kwargs):
        """
        Bind arguments to a Runnable, returning a new Runnable.
        """
        return RunnableBinding(bound=self, kwargs=kwargs)

    def map(self):
        """
        Return a new Runnable that maps a list of inputs to a list of outputs,
        by calling invoke() with each input.
        """
        return RunnableEach(bound=self)



    def _get_config_list(
        self, config, length: int
    ):
        """
        Helper method to get a list of configs from a single config or a list of
        configs, useful for subclasses overriding batch() or abatch().
        """
        if length < 1:
            raise ValueError(f"length must be >= 1, but got {length}")
        if isinstance(config, list) and len(config) != length:
            raise ValueError(
                f"config must be a list of the same length as inputs, "
                f"but got {len(config)} configs for {length} inputs"
            )

        return (
            list(map(ensure_config, config))
            if isinstance(config, list)
            else [patch_config(config, deep_copy_locals=True) for _ in range(length)]
        )

    def _call_with_config(
        self,
        func,
        input,
        config,
        run_type,
    ):
        """Helper method to transform an Input value to an Output value,
        with callbacks. Use this method to implement invoke() in subclasses."""
        config = ensure_config(config)
        callback_manager = get_callback_manager_for_config(config)
        run_manager = callback_manager.on_chain_start(
            dumpd(self),
            input,
            run_type=run_type,
        )
        try:
            if accepts_run_manager_and_config(func):
                output = func(
                    input,
                    run_manager=run_manager,
                    config=config,
                )  # type: ignore[call-arg]
            elif accepts_run_manager(func):
                output = func(input, run_manager=run_manager)  # type: ignore[call-arg]
            else:
                output = func(input)  # type: ignore[call-arg]
        except Exception as e:
            run_manager.on_chain_error(e)
            raise
        else:
            run_manager.on_chain_end(dumpd(output))
            return output

class RunnableEach(Serializable, Runnable):
    """
    A runnable that delegates calls to another runnable
    with each element of the input sequence.
    """
    class Config:
        arbitrary_types_allowed = True

    def invoke(
        self, input: List[Input], config
    ):
        return self.bound.batch(input, config)

    async def ainvoke(
        self, input: List[Input], config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> List[Output]:
        return await self.bound.abatch(input, config, **kwargs)

class RunnableSequence(Serializable, Runnable):
    """
    A sequence of runnables, where the output of each is the input of the next.
    """

    class Config:
        arbitrary_types_allowed = True

    def __or__(
        self,
        other,
    ):
        if isinstance(other, RunnableSequence):
            return RunnableSequence(
                first=self.first,
                middle=self.middle + [self.last] + [other.first] + other.middle,
                last=other.last,
            )
        else:
            return RunnableSequence(
                first=self.first,
                middle=self.middle + [self.last],
                last=coerce_to_runnable(other),
            )

    def __ror__(
        self,
        other,
    ):
        if isinstance(other, RunnableSequence):
            return RunnableSequence(
                first=other.first,
                middle=other.middle + [other.last] + [self.first] + self.middle,
                last=self.last,
            )
        else:
            return RunnableSequence(
                first=coerce_to_runnable(other),
                middle=[self.first] + self.middle,
                last=self.last,
            )

    def invoke(self, input: Input, config) -> Output:
        # setup callbacks
        config = ensure_config(config)
        callback_manager = get_callback_manager_for_config(config)
        # start the root run
        run_manager = callback_manager.on_chain_start(dumpd(self), input)

        # invoke all steps in sequence
        try:
            for step in self.steps:
                input = step.invoke(
                    input,
                    # mark each step as a child run
                    patch_config(config, callbacks=run_manager.get_child()),
                )
        # finish the root run
        except (KeyboardInterrupt, Exception) as e:
            run_manager.on_chain_error(e)
            raise
        else:
            run_manager.on_chain_end(input)
            return cast(Output, input)

    def batch(
        self,
        inputs: List[Input],
        config,
        **kwargs: Optional[Any],
    ) -> List[Output]:
        from langchain.callbacks.manager import CallbackManager   #We need to also rewrite this class today.

        # setup callbacks
        configs = self._get_config_list(config, len(inputs))
        callback_managers = [
            CallbackManager.configure(
                inheritable_callbacks=config.get("callbacks"),
                local_callbacks=None,
                verbose=False,
                inheritable_tags=config.get("tags"),
                local_tags=None,
                inheritable_metadata=config.get("metadata"),
                local_metadata=None,
            )
            for config in configs
        ]
        # start the root runs, one per input
        run_managers = [
            cm.on_chain_start(dumpd(self), input)
            for cm, input in zip(callback_managers, inputs)
        ]

        # invoke
        try:
            for step in self.steps:
                inputs = step.batch(
                    inputs,
                    [
                        # each step a child run of the corresponding root run
                        patch_config(config, callbacks=rm.get_child())
                        for rm, config in zip(run_managers, configs)
                    ],
                )
        # finish the root runs
        except (KeyboardInterrupt, Exception) as e:
            for rm in run_managers:
                rm.on_chain_error(e)
            raise
        else:
            for rm, input in zip(run_managers, inputs):
                rm.on_chain_end(input)
            return cast(List[Output], inputs)

    async def abatch(
        self,
        inputs: List[Input],
        config: Optional[Union[RunnableConfig, List[RunnableConfig]]] = None,
        **kwargs: Optional[Any],
    ) -> List[Output]:
        from langchain.callbacks.manager import (
            AsyncCallbackManager,
        )

        # setup callbacks
        configs = self._get_config_list(config, len(inputs))
        callback_managers = [
            AsyncCallbackManager.configure(
                inheritable_callbacks=config.get("callbacks"),
                local_callbacks=None,
                verbose=False,
                inheritable_tags=config.get("tags"),
                local_tags=None,
                inheritable_metadata=config.get("metadata"),
                local_metadata=None,
            )
            for config in configs
        ]
        # start the root runs, one per input
        run_managers: List[AsyncCallbackManagerForChainRun] = await asyncio.gather(
            *(
                cm.on_chain_start(dumpd(self), input)
                for cm, input in zip(callback_managers, inputs)
            )
        )

        # invoke .batch() on each step
        # this uses batching optimizations in Runnable subclasses, like LLM
        try:
            for step in self.steps:
                inputs = await step.abatch(
                    inputs,
                    [
                        # each step a child run of the corresponding root run
                        patch_config(config, callbacks=rm.get_child())
                        for rm, config in zip(run_managers, configs)
                    ],
                )
        # finish the root runs
        except (KeyboardInterrupt, Exception) as e:
            await asyncio.gather(*(rm.on_chain_error(e) for rm in run_managers))
            raise
        else:
            await asyncio.gather(
                *(rm.on_chain_end(input) for rm, input in zip(run_managers, inputs))
            )
            return cast(List[Output], inputs)

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        # setup callbacks
        config = ensure_config(config)
        callback_manager = get_callback_manager_for_config(config)
        # start the root run
        run_manager = callback_manager.on_chain_start(dumpd(self), input)

        steps = [self.first] + self.middle + [self.last]
        streaming_start_index = 0

        for i in range(len(steps) - 1, 0, -1):
            if type(steps[i]).transform != Runnable.transform:
                streaming_start_index = i - 1
            else:
                break

        # invoke the first steps
        try:
            for step in steps[0:streaming_start_index]:
                input = step.invoke(
                    input,
                    # mark each step as a child run
                    patch_config(config, callbacks=run_manager.get_child()),
                )
        except (KeyboardInterrupt, Exception) as e:
            run_manager.on_chain_error(e)
            raise

        # stream the last steps
        final: Union[Output, None] = None
        final_supported = True
        try:
            # stream the first of the last steps with non-streaming input
            final_pipeline = steps[streaming_start_index].stream(
                input, patch_config(config, callbacks=run_manager.get_child())
            )
            # stream the rest of the last steps with streaming input
            for step in steps[streaming_start_index + 1 :]:
                final_pipeline = step.transform(
                    final_pipeline,
                    patch_config(config, callbacks=run_manager.get_child()),
                )
            for output in final_pipeline:
                yield output
                # Accumulate output if possible, otherwise disable accumulation
                if final_supported:
                    if final is None:
                        final = output
                    else:
                        try:
                            final += output  # type: ignore[operator]
                        except TypeError:
                            final = None
                            final_supported = False
                            pass
        # finish the root run
        except (KeyboardInterrupt, Exception) as e:
            run_manager.on_chain_error(e)
            raise
        else:
            run_manager.on_chain_end(final)

    async def astream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> AsyncIterator[Output]:
        # setup callbacks
        config = ensure_config(config)
        callback_manager = get_async_callback_manager_for_config(config)
        # start the root run
        run_manager = await callback_manager.on_chain_start(dumpd(self), input)

        steps = [self.first] + self.middle + [self.last]
        streaming_start_index = len(steps) - 1

        for i in range(len(steps) - 1, 0, -1):
            if type(steps[i]).transform != Runnable.transform:
                streaming_start_index = i - 1
            else:
                break

        # invoke the first steps
        try:
            for step in steps[0:streaming_start_index]:
                input = await step.ainvoke(
                    input,
                    # mark each step as a child run
                    patch_config(config, callbacks=run_manager.get_child()),
                )
        except (KeyboardInterrupt, Exception) as e:
            await run_manager.on_chain_error(e)
            raise

        # stream the last steps
        final: Union[Output, None] = None
        final_supported = True
        try:
            # stream the first of the last steps with non-streaming input
            final_pipeline = steps[streaming_start_index].astream(
                input, patch_config(config, callbacks=run_manager.get_child())
            )
            # stream the rest of the last steps with streaming input
            for step in steps[streaming_start_index + 1 :]:
                final_pipeline = step.atransform(
                    final_pipeline,
                    patch_config(config, callbacks=run_manager.get_child()),
                )
            async for output in final_pipeline:
                yield output
                # Accumulate output if possible, otherwise disable accumulation
                if final_supported:
                    if final is None:
                        final = output
                    else:
                        try:
                            final += output  # type: ignore[operator]
                        except TypeError:
                            final = None
                            final_supported = False
                            pass
        # finish the root run
        except (KeyboardInterrupt, Exception) as e:
            await run_manager.on_chain_error(e)
            raise
        else:
            await run_manager.on_chain_end(final)




class RunnableBinding(Serializable, Runnable):
    """
    A runnable that delegates calls to another runnable with a set of kwargs.
    """
    class Config:
        arbitrary_types_allowed = True

    @property
    def lc_serializable(self) -> bool:
        return True

    @property
    def lc_namespace(self) -> List[str]:
        return self.__class__.__module__.split(".")[:-1]

    def bind(self, **kwargs: Any):
        return self.__class__(bound=self.bound, kwargs={**self.kwargs, **kwargs})

    def invoke(
        self,
        input,
        config,
        **kwargs,
    ):
        return self.bound.invoke(input, config, **{**self.kwargs, **kwargs})
    def batch(
        self,
        inputs,
        config,
        **kwargs,
    ):
        return self.bound.batch(inputs, config, **{**self.kwargs, **kwargs})

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        yield from self.bound.stream(input, config, **{**self.kwargs, **kwargs})

    async def astream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> AsyncIterator[Output]:
        async for item in self.bound.astream(
            input, config, **{**self.kwargs, **kwargs}
        ):
            yield item

    def transform(
        self,
        input: Iterator[Input],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Iterator[Output]:
        yield from self.bound.transform(input, config, **{**self.kwargs, **kwargs})

    async def atransform(
        self,
        input: AsyncIterator[Input],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> AsyncIterator[Output]:
        async for item in self.bound.atransform(
            input, config, **{**self.kwargs, **kwargs}
        ):
            yield item


def coerce_to_runnable(
    thing: Union[
        Runnable[Input, Output],
        Callable[[Input], Output],
        Mapping[str, Any],
    ]
):
    if isinstance(thing, Runnable):
        return thing
    elif callable(thing):
        return RunnableLambda(thing)
    elif isinstance(thing, dict):
        runnables: Mapping[str, Runnable[Any, Any]] = {
            key: coerce_to_runnable(r) for key, r in thing.items()
        }
        return cast(Runnable[Input, Output], RunnableMap(steps=runnables))
    else:
        raise TypeError(
            f"Expected a Runnable, callable or dict."
            f"Instead got an unsupported type: {type(thing)}"
        )

