from pydantic import Extra, root_validator
from typing import List, Optional, Dict, Any
from base_chain import Chain
from pydantic import root_validator
from typing import List

class SimpleSequentialChain(Chain):
    chains: List[Chain]
    strip_outputs: bool = False
    input_keys_alias: str = "input"  #: :meta private:
    output_key_alias: str = "output"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys_alias(self) -> List[str]:
        """Expect input key.

        :meta private:
        """
        return [self.input_keys_alias]

    @property
    def output_key_alias(self) -> List[str]:
        """Return output key.

        :meta private:
        """
        return [self.output_key_alias]

    @root_validator(pre=True)
    def validate_chains(cls, values):
        chains = values.get('chains')
        if chains is None:
            raise ValueError('"chains" must be provided')
        for chain in chains:
            # Check if 'input_keys' and 'output_key_alias' attributes exist
            if not hasattr(chain, 'input_keys_alias') or not hasattr(chain, 'output_key_alias'):
                raise ValueError(f"The object {chain} doesn't have input_keys_alias and/or output_key attributes.")
            """
            if len(chain.input_keys_alias) != 1 or len(chain.output_key_alias) != 1:
                raise ValueError(
                    f"Chains in SimpleSequentialChain should all have one input and one output, got {chain} with {len(chain.input_keys_alias)} inputs and {len(chain.output_key_alias)} outputs."
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
        return {self.output_key_alias[0]: output}  # Assuming there's only one output key
