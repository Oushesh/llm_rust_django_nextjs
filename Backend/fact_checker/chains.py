from pydantic import Extra, root_validator
from typing import List, Optional, Dict, Any
from base_chain import Chain
from pydantic import root_validator
from typing import List

class SimpleSequentialChain(Chain):
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

    @root_validator(pre=True)
    def validate_chains(cls, values):
        chains = values.get('chains')
        if chains is None:
            raise ValueError('"chains" must be provided')
        for chain in chains:
            # Check if 'input_keys' and 'output_keys' attributes exist
            if not hasattr(chain, 'input_keys') or not hasattr(chain, 'output_keys'):
                raise ValueError(f"The object {chain} doesn't have input_keys and/or output_keys attributes.")
            """
            if len(chain.input_keys) != 1 or len(chain.output_keys) != 1:
                raise ValueError(
                    f"Chains in SimpleSequentialChain should all have one input and one output, got {chain} with {len(chain.input_keys)} inputs and {len(chain.output_keys)} outputs."
                )
            """
        return values


    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        _run_manager = run_manager
        output = inputs
        color_mapping = get_color_mapping([str(i) for i in range(len(self.chains))])  # Assuming get_color_mapping is defined elsewhere
        for i, chain in enumerate(self.chains):
            output = chain.run(output, callbacks=_run_manager.get_child(f"step_{i+1}"))
            if self.strip_outputs:
                output = output.strip()
            _run_manager.on_text(
                output, color=color_mapping[str(i)], end="\n", verbose=self.verbose
            )
        return {self.output_keys[0]: output}  # Assuming there's only one output key
