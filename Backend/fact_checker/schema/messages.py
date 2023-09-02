from schema_serializable import Serializable
from pydantic import Field
from typing import Any, Dict
from abc import ABC, abstractmethod
class BaseMessage(Serializable):
    """The base abstract Message class.

    Messages are the inputs and outputs of ChatModels.
    """

    content: str
    """The string contents of the message."""

    additional_kwargs: dict = Field(default_factory=dict)
    """Any additional information."""

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the Message, used for serialization."""

    @property
    def lc_serializable(self) -> bool:
        """Whether this class is LangChain serializable."""
        return True

    def __add__(self, other: Any):
        from langchain.prompts.chat import ChatPromptTemplate

        prompt = ChatPromptTemplate(messages=[self])
        return prompt + other