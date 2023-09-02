from typing import List, Optional, Dict, Any
from base_chain import Chain
from pydantic import Extra, root_validator

class SimpleSequentialChain(Chain):
    def __init__(self, *, chains=None):
        self.components = chains

    @property
    def input_keys(self) -> List[str]:
        # Assuming the first component dictates the input keys
        return self.components[0].input_keys

    @property
    def output_keys(self) -> List[str]:
        # Assuming the last component dictates the output keys
        return self.components[-1].output_keys

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        # Implement the logic to call the components in sequence
        output = inputs
        for component in self.components:
            output = component(output)
        return output


    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator()
    def validate_chains(cls, values: Dict):     #class method: this is called even without instantiating the
        """Validate that chains are all single input/output."""
        value_chain =values.get("chains",{})
        if not value_chain=={}:
            for chain in value_chain:
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
        run_manager=None,
    ):
        print("Debug: Instance Attributes:", self.__dict__)  # Debugging statement
        print("Debug: Is Instance of SimpleSequentialChain:", isinstance(self, SimpleSequentialChain))  # Debugging statement

        _run_manager = run_manager
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
