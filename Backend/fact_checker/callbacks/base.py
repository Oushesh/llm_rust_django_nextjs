from typing import List, Dict, Any, Optional, Union
import uuid
from uuid import UUID

class CallbackManagerMixin:
    """Mixin for callback manager."""

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a chat model starts running."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement `on_chat_model_start`"
        )

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when Retriever starts running."""

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain starts running."""

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""

#TODO: remove all basehandler or basehandlers Oushesh (refactor)
class BaseCallbackManager(CallbackManagerMixin):
    """Base callback manager that handles callbacks from LangChain."""

    def __init__(
        self,
        handlers,
        inheritable_handlers,
        parent_run_id,
        *,
        tags,
        inheritable_tags,
        metadata,
        inheritable_metadata,
    ) -> None:
        """Initialize callback manager."""
        self.handlers = handlers
        self.inheritable_handlers= (
            inheritable_handlers or []
        )
        self.parent_run_id = parent_run_id
        self.tags = tags or []
        self.inheritable_tags = inheritable_tags or []
        self.metadata = metadata or {}
        self.inheritable_metadata = inheritable_metadata or {}

    @property
    def is_async(self) -> bool:
        """Whether the callback manager is async."""
        return False

    def add_handler(self, handler, inherit: bool = True) -> None:
        """Add a handler to the callback manager."""
        if handler not in self.handlers:
            self.handlers.append(handler)
        if inherit and handler not in self.inheritable_handlers:
            self.inheritable_handlers.append(handler)

    def remove_handler(self, handler) -> None:
        """Remove a handler from the callback manager."""
        self.handlers.remove(handler)
        self.inheritable_handlers.remove(handler)

    def set_handlers(
        self, handlers, inherit: bool = True
    ) -> None:
        """Set handlers as the only handlers on the callback manager."""
        self.handlers = []
        self.inheritable_handlers = []
        for handler in handlers:
            self.add_handler(handler, inherit=inherit)

    def set_handler(self, handler, inherit: bool = True) -> None:
        """Set handler as the only handler on the callback manager."""
        self.set_handlers([handler], inherit=inherit)

    def add_tags(self, tags: List[str], inherit: bool = True) -> None:
        for tag in tags:
            if tag in self.tags:
                self.remove_tags([tag])
        self.tags.extend(tags)
        if inherit:
            self.inheritable_tags.extend(tags)

    def remove_tags(self, tags: List[str]) -> None:
        for tag in tags:
            self.tags.remove(tag)
            self.inheritable_tags.remove(tag)

    def add_metadata(self, metadata: Dict[str, Any], inherit: bool = True) -> None:
        self.metadata.update(metadata)
        if inherit:
            self.inheritable_metadata.update(metadata)

    def remove_metadata(self, keys: List[str]) -> None:
        for key in keys:
            self.metadata.pop(key)
            self.inheritable_metadata.pop(key)


#TODO: Removed all BaseCallBackHandler Arguments
class BaseCallbackHandler():
    """Base callback handler that can be used to handle callbacks from langchain."""

    raise_error: bool = False

    run_inline: bool = False

    @property
    def ignore_llm(self) -> bool:
        """Whether to ignore LLM callbacks."""
        return False

    @property
    def ignore_retry(self) -> bool:
        """Whether to ignore retry callbacks."""
        return False

    @property
    def ignore_chain(self) -> bool:
        """Whether to ignore chain callbacks."""
        return False

    @property
    def ignore_agent(self) -> bool:
        """Whether to ignore agent callbacks."""
        return False

    @property
    def ignore_retriever(self) -> bool:
        """Whether to ignore retriever callbacks."""
        return False

    @property
    def ignore_chat_model(self) -> bool:
        """Whether to ignore chat model callbacks."""
        return False

Callbacks = Optional[Union[List[BaseCallbackHandler], BaseCallbackManager]]