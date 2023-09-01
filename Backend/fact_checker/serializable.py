from typing import List, Dict, Any, Optional, Union, cast
from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr

from pydantic import BaseModel, PrivateAttr, Extra
from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast

class Serializable(BaseModel, ABC):
    """Serializable base class."""
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def lc_serializable(self) -> bool:
        """
        Return whether or not the class is serializable.
        """
        return False

    @property
    def lc_namespace(self) -> List[str]:
        """
        Return the namespace of the langchain object.
        eg. ["langchain", "llms", "openai"]
        """
        return self.__class__.__module__.split(".")

    @property
    def lc_secrets(self) -> Dict[str, str]:
        """
        Return a map of constructor argument names to secret ids.
        eg. {"openai_api_key": "OPENAI_API_KEY"}
        """
        return dict()

    @property
    def lc_attributes(self) -> Dict:
        """
        Return a list of attribute names that should be included in the
        serialized kwargs. These attributes must be accepted by the
        constructor.
        """
        return {}

    class Config:
        extra = "ignore"  # this allows for extra fields to be ignored

    _lc_kwargs = PrivateAttr(default_factory=dict)

    # Implementing required abstract methods (replace with actual methods if needed)
    @abstractmethod
    def _call(self):
        pass

    @abstractmethod
    def input_keys(self):
        pass

    @abstractmethod
    def output_keys(self):
        pass

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)  # calling the constructor of the superclass
        self._lc_kwargs = kwargs    # storing kwargs



    def to_json(self):
        if not self.lc_serializable:
            return self.to_json_not_implemented()

        secrets = dict()
        # Get latest values for kwargs if there is an attribute with same name
        lc_kwargs = {
            k: getattr(self, k, v)
            for k, v in self._lc_kwargs.items()
            if not (self.__exclude_fields__ or {}).get(k, False)  # type: ignore
        }

        # Merge the lc_secrets and lc_attributes from every class in the MRO
        for cls in [None, *self.__class__.mro()]:
            # Once we get to Serializable, we're done
            if cls is Serializable:
                break

            # Get a reference to self bound to each class in the MRO
            this = cast(Serializable, self if cls is None else super(cls, self))

            secrets.update(this.lc_secrets)
            lc_kwargs.update(this.lc_attributes)

        # include all secrets, even if not specified in kwargs
        # as these secrets may be passed as an environment variable instead
        for key in secrets.keys():
            secret_value = getattr(self, key, None) or lc_kwargs.get(key)
            if secret_value is not None:
                lc_kwargs.update({key: secret_value})

        return {
            "lc": 1,
            "type": "constructor",
            "id": [*self.lc_namespace, self.__class__.__name__],
            "kwargs": lc_kwargs
            if not secrets
            else _replace_secrets(lc_kwargs, secrets),
        }

    def to_json_not_implemented(self):
        return to_json_not_implemented(self)

