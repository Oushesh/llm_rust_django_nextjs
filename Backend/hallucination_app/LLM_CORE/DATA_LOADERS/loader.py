# Custom document loaders
# Converts a pdf into a list of elements
# Reference: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/document_loaders/unstructured.py
from typing import Dict, Iterator

import sys
import os

# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the project root directory (three levels up from loaders.py)
project_root = os.path.abspath(os.path.join(current_script_dir, "../../../.."))

# print("project_root", project_root)
# Add the project root to PYTHONPATH
sys.path.append(project_root)

from Backend.hallucination_app.LLM_CORE.PREPROCESSING.preprocessor import *


class BaseLoader(ABC):
    """Interface for Document loader.
    Implementations should implement
    the lazy-loading using the generators

    The 'load' method will remain as is for
    backwards compatibility, implementation
    should be just 'list(self.lazy_load())'
    r"""

    @abstractmethod
    def load(self) -> List[Document]:
        """load data into Document Objects"""

    def load_and_split(self, text_splitter=None) -> List[Document]:
        """Load Documents and split into chunks.
        Chunks are returned as Documents.

        Args:
            text_splitter: Text Splitter instance to use for splitting Document.
        """
        if text_splitter is None:
            _text_splitter: TextSplitter = RecursiveCharacterTextSplitter()
        else:
            _text_splitter = text_splitter
        docs = self.load()
        return _text_splitter.split_documents(docs)

    # TODO: implement the lazyload for the documents.
    def lazy_load(self) -> Iterator[Document]:
        """A lazy loader for Documents."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement lazy_load()"
        )


class UnstructuredBaseLoader(BaseLoader, ABC):
    """Base Loader that uses 'Unstructured.'"""


class UnstructuredFileLoader(UnstructuredBaseLoader):
    """Load Files using Unstructured
    Example:
        loader = UnstructuredFileLoader(
        ".pdf file", mode="elements", strategy="fast"

    docs = loader.load()
    References: https://unstructured-io.github.io/unstructured/bricks.html#partition
    ------------
    """

    def __init__(
        self,
        file_path: List[str],
        mode: str = "single",
        **kwargs: Any,
    ):
        """Initialize with file path."""
        self.file_path = file_path
        super().__init__(mode=mode, **kwargs)

    def _get_elements(self) -> List:
        from unstructured.partition.auto import partition

        return partition(filename=self.file_path, **self.kwargs)

    def _get_metadata(self) -> dict:
        return {"source": self.file_path}


class Data_loader(UnstructuredFileLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if "text/html content not found in email" in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"] = "text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e
        return doc


# Reference: https://github.com/Unstructured-IO/unstructured/tree/main


class CSVLoader(BaseLoader):
    """Load a `CSV` file into a list of Documents.

    Each document represents one row of the CSV file. Every row is converted into a
    key/value pair and outputted to a new line in the document's page_content.

    The source for each document loaded from csv is set to the value of the
    `file_path` argument for all documents by default.
    You can override this by setting the `source_column` argument to the
    name of a column in the CSV file.
    The source of each document will then be set to the value of the column
    with the name specified in `source_column`.

    Output Example:
        .. code-block:: txt

            column1: value1
            column2: value2
            column3: value3
    """

    def __init__(
        self,
        file_path: str,
        source_column: Optional[str] = None,
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
    ):
        """

        Args:
            file_path: The path to the CSV file.
            source_column: The name of the column in the CSV file to use as the source.
              Optional. Defaults to None.
            csv_args: A dictionary of arguments to pass to the csv.DictReader.
              Optional. Defaults to None.
            encoding: The encoding of the CSV file. Optional. Defaults to None.
        """
        self.file_path = file_path
        self.source_column = source_column
        self.encoding = encoding
        self.csv_args = csv_args or {}

    def load(self) -> List[Document]:
        """Load data into document objects."""

        docs = []
        with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)  # type: ignore
            for i, row in enumerate(csv_reader):
                content = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in row.items())
                try:
                    source = (
                        row[self.source_column]
                        if self.source_column is not None
                        else self.file_path
                    )
                except KeyError:
                    raise ValueError(
                        f"Source column '{self.source_column}' not found in CSV file."
                    )
                metadata = {"source": source, "row": i}
                doc = Document(page_content=content, metadata=metadata)
                docs.append(doc)

        return docs
