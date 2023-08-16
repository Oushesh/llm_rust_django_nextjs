import csv
from abc import ABC, abstractmethod
from typing import Iterator,Any,List,Optional,Dict
from langchain.schema import Document
import os


def _get_prompt_and_tools(
        df:Any,
        prefix: Optional[str]=None,
        suffix: OPtional[str]=None,
        input_variables: Optional[List[str]] = None,
        include_df_in_prompt: Optional[bool] = True,
        number_of_head_rows: int = 5
):
    try:
        import pandas as pd

        pd.set_option("display.max_columns",None)
    except ImportError:
        raise ImportError(
            "pandas package not found, please install with 'pip install pandas'"
        )

    #Handles the Case we have lots of panda DataFrames. Example: list of pandas dataframe
    if isinstance(df,list):
        for item in df:
            if not isinstance(item,pd.DataFrame):
                raise ValueError(f"Expected pandas Object, got {type(df)}")

    else:
        if not isinstance(df,pd.DataFrame):
            raise ValueError(f"Expected pandas Object, got{type(df)}")

        return _get_single_prompt(
            df,
            prefix=prefix,
            suffix=suffix,
            input_variables=input_variables,
            include_df_in_prompt=include_df_in_prompt,
            number_of_head_rows=number_of_head_rows,
        )

class Pandas_Agent:
    """
    Create a Pandas_Agent
    from pandas dataframe which will
    be used by other agents like the CSV
    """
    def __init__(self,**kwargs):
        self.llm = kwargs.get('llm',None)
        self.df = kwargs.get('df',None)
        self.verbose = kwargs.get('verbose',None)

    @classmethod
    def create_pandas_dataframe_agent(cls,
        llm: BaseLanguageModel,
        df: Any,
        verbose: bool,
        ) -> AgentExecutor:
        """
        :param llm: Type BaseLanguageModel
        :param df:  pandas dataframe
        :param verbose: bool
        :return: AgentExecutor type
        """
        return None
class BaseLanguageModel:
    """
    Abstract base class for interfacing
    with language models.

    All language model wrappers inherit from
    BaseLanguageModel. At least,expected.

    Exposes the following methods:
    - generate_prompt: generate language model
    outputs for a sequence of prompt. (string type)

    - predict: pass in a single string to
    a language model and return a string
    prediction.
    """

    @abstractmethod
    async def predict(self,
        messages:List[BaseMessage],
        *,
        stop: Optional[Sequence[str]] = None,
        **kwargs: Any,
        ) -> BaseMessage:
        """
        Pass a message sequence to the model
        and return a message prediction.
        Use this method when passing in
        chat messages. If you pass in a
        raw text, use predict.

        Args:
         messages: A sequence of chat messages
         corresponding to a single model input.
         stop: Stop words to use when generating.
         Model output is cut off at the first
         occurrence of any of those substrings.

        :param messages:
        :param stop:
        :param kwargs:
        :return:
        """


class CSV_Agent:
    def __init__(self,**kwargs):
        self.llm = kwargs.get('llm',None)
        self.path = kwargs.get('path',None)
        self.pandas_kwargs: Optional[dict] = None,

    @classmethod
    def create_csv_agent(cls,**kwargs) ->AgentExecutor:
        llm: BaseLanguageModel,
        path:
        pandas_kwargs:

class CSV_Loader:
    def __init__(self,**kwargs):
        self.filename = kwargs.get('filename',None) #kwargs['filename']
        self.delimiter = kwargs.get('delimiter',None)
        self.encoding = kwargs.get('encoding',None)

    #Pass all the other names here if needed.
    @classmethod
    def lazy_csv_loader(cls,*args):
        with open(filename,'r') as csvfile:
            csvreader = csv.reader(csvfile)
            #Skip the header row if present
            next(csvreader,None)

            for row in csvreader:
                yield row
        return None

if __name__ == "__main__":
    filedir = "../DATA"
    filename = "dataset_inventory_2018_03_11.csv"
    filepath = os.path.join(filedir,filename)
    print (filepath)
    CSV_Loader(filename="data.csv",delimiter=",",encoding="utf-8").lazy_csv_loader(filename)

