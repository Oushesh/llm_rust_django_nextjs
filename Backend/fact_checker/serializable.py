from abc import ABC, abstractmethod
from pydantic import BaseModel, Extra, PrivateAttr
from typing import Any, List, Dict, cast

# Dummy implementation of unimplemented functions
def to_json_not_implemented(obj):
    return f"{obj.__class__.__name__} serialization is not implemented"

def _replace_secrets(lc_kwargs, secrets):
    return lc_kwargs  # Dummy implementation

class Serializable(BaseModel, ABC):
    """Serializable base class."""

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.ignore  # Changed to ignore
        arbitrary_types_allowed = True

    @property
    def lc_serializable(self) -> bool:
        return False

    @property
    def lc_namespace(self) -> List[str]:
        return self.__class__.__module__.split(".")

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return dict()

    @property
    def lc_attributes(self) -> Dict:
        return {}

    _lc_kwargs = PrivateAttr(default_factory=dict)

    @abstractmethod
    def _call(self):
        pass

    @abstractmethod
    def input_keys_alias(self) -> List[str]:
        pass

    @abstractmethod
    def output_key_alias(self) -> List[str]:
        pass

    def __init__(self, **kwargs: Any):
        print("Debug kwargs:", kwargs)  # Debugging line
        self._lc_kwargs = kwargs

    def to_json(self):
        if not self.lc_serializable:
            return self.to_json_not_implemented()

        secrets = dict()
        lc_kwargs = {k: getattr(self, k, v) for k, v in self._lc_kwargs.items() if not (self.__exclude_fields__ or {}).get(k, False)}

        for cls in [None, *self.__class__.mro()]:
            if cls is Serializable:
                break
            this = cast(Serializable, self if cls is None else super(cls, self))
            secrets.update(this.lc_secrets)
            lc_kwargs.update(this.lc_attributes)

        for key in secrets.keys():
            secret_value = getattr(self, key, None) or lc_kwargs.get(key)
            if secret_value is not None:
                lc_kwargs.update({key: secret_value})

        return {
            "lc": 1,
            "type": "constructor",
            "id": [*self.lc_namespace, self.__class__.__name__],
            "kwargs": lc_kwargs if not secrets else _replace_secrets(lc_kwargs, secrets),
        }

    def to_json_not_implemented(self):
        return to_json_not_implemented(self)
