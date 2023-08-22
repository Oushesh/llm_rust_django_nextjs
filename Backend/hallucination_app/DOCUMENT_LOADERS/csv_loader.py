import csv
from typing import Any, Dict, List, Optional

import Backend
from Backend.hallucination_app.DOCUMENT_LOADERS.base import BaseLoader
from Backend.hallucination_app.schema.document import Document

class CSVLoader(BaseLoader):
    """
    Load a CSV File into a list of Documents
    Each document represents 1 row of CSV file.
    Every row is converted into a key/value pair
    and output to a new line in the document's
    page_content.
    """
    def __int__(self,
                file_path:str,
                source_column: Optional[str]=None,
                csv_args: Optional[Dict] = None,
                encoding: Optional[str] = None,
                ):
        """
        :param file_path: The path to CSV file.
        :param source_column: name of column in CSV file to use as source
        :param csv_args: Dictionary of arguments to pass to the csv.DictReader.
        :param encoding: encoding of CSV file.
        :return:
        """

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

#Test the document loader:
if __name__ == "__main__":
    #TBD







