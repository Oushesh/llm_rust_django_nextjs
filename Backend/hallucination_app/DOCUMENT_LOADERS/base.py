"""
Abstract interface for document loader
implementations.
"""
from abc import ABC, abstractmethod
from typing import Iterator, List, Optional


class BaseLoader(ABC):
    """
    Interface for Document Loader.

    Implementations should implement
    the lazy-loading method using
    generators to avoid loading all
    Documents into memory at once.

    The source for each document loaded
    from csv is set to the value of "file_path"
    """

    def __init__(
            self,
            file_path: str,
            source_column: Optional[str] = None,
            csv_args: Optional[str] = None,
            encoding: Optional[str] = None,
            ):
        """
        :param file_path: The path to the CSV file
        :param source_column: The name of the column in csv file to use as source.
        :param csv_args: dictionary of arguments to pass to csv.DictReader.
        :param encoding:
        """
        self.file_path = file_path
        self.source_column = source_column
        self.encoding = encoding
        self.csv_args = csv_args or {}

    """
    A lazy loader for Documents.
    """
    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader for Documents."""
        raise NotImplementedError(
            f"{self} does not implement lazy_load()"
        )


