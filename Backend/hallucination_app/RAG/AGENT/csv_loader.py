import csv
from typing import Any,List,Optional, Dict

from langchain.document_loaders.blob_loaders import Blob
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter


class BaseLoader(ABC):
    """
    Interface for Document Loader.
    Implementations should implement
    the lazy-loading method once using
    generators to avoid all Documents
    into memory at once. (Generators)
    """

def lazy_csv_loader(filename):
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        #Skip the header row if present
        next(csvreader,None)

        for row in csvreader:
            yield row

    return None

#Usage
csv_filename