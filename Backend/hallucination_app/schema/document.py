from __future__ import annotations
from pydantic import Field
from abc import ABC, abstractmethod
from typing import Any, Sequence
import Backend
from Backend.hallucination_app.INGESTION.Serializable import Serializable

class Document(Serializable):
    """Class for storing a piece of text and associated metadata."""
    page_content: str
    """String text."""
    metadata: dict = Field(default_factory=dict)
    """
    Arbitrary metadata about the page content (e.g. source,
    relationships to other documents, etc.).
    """

class BaseDocumentTransformer(ABC):
    """
    Abstract base class for document transformation
    systems.
    A document transformation system takes
    a sequence of Documents and returns a sequence
    of transformed Documents.
    """

    @abstractmethod
    def transform_documents(
            self,
            documents: Sequence[Document],
            **kwargs:Any
    ) -> Sequence[Document]:
        """
        Transform a list of documents.
        :param documents: A sequence of documents to be transformed
        :param kwargs:
        :return: A list of transformed documents
        """

    @abstractmethod
    async def atransform_documents(
            self,
            documents: Sequence[Document],
            **kwargs: Any
    )->Sequence[Document]:
        """
        Asynchronously transform a list of documents
        :param documents: A sequence of Documents to be transformed.
        :param kwargs:
        :return:
        A list of transformed Documents
        """
