from abc import ABC
from pydantic import BaseModel
from typing import List, Dict

class Serializable(BaseModel,ABC):
    """ Serializable Base Class."""

    @property
    def lc_serializable(self) -> bool:
        """
        :return: whether or not the class
        is serializable
        """
        return False

    @property
    def lc_namespace(self)-> List[str]:
        """
        Return the namespace of the langchain
        object.
        :return:
        """
        return self.__class__.__module__.split(".")

    @property
    def lc_secrets(self)-> Dict[str,str]:
        """
        :return: a map of constructor argument
        names to secret ids.
        eg: {"openai_api_key:"OPEN_API_KEY"}
        """
        return dict()

    @property
    def lc_attributes(self)->Dict:
        """
        Return a list of attribute names that
        should be included in the serialized kwargs.
        These attributes must be accepted by the
        constructor.
        :return:
        """
        return {}





