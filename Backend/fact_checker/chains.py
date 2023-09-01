from typing import List, Optional, Dict
from base_chain import Chain
class SimpleSequentialChain(Chain):
    """Simple chain where the outputs of one step feed directly into next."""

    chains: List[Chain]
    strip_outputs: bool = False
    input_key: str = "input"  #: :meta private:
    output_key: str = "output"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Return output key.

        :meta private:
        """
        return [self.output_key]

    @root_validator()
    def validate_chains(cls, values: Dict) -> Dict:
        """Validate that chains are all single input/output."""
        for chain in values["chains"]:
            if len(chain.input_keys) != 1:
                raise ValueError(
                    "Chains used in SimplePipeline should all have one input, got "
                    f"{chain} with {len(chain.input_keys)} inputs."
                )
            if len(chain.output_keys) != 1:
                raise ValueError(
                    "Chains used in SimplePipeline should all have one output, got "
                    f"{chain} with {len(chain.output_keys)} outputs."
                )
        return values

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        _input = inputs[self.input_key]
        color_mapping = get_color_mapping([str(i) for i in range(len(self.chains))])
        for i, chain in enumerate(self.chains):
            _input = chain.run(_input, callbacks=_run_manager.get_child(f"step_{i+1}"))
            if self.strip_outputs:
                _input = _input.strip()
            _run_manager.on_text(
                _input, color=color_mapping[str(i)], end="\n", verbose=self.verbose
            )
        return {self.output_key: _input}
