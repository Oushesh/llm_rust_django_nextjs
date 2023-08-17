import csv
from abc import ABC, abstractmethod
from typing import Iterator,Any,List,Optional,Dict
from langchain.schema import Document
import os
import pandas as pd

class CSV_Loader:
    def __init__(self,**kwargs):
        self.filepath = kwargs.get('filepath',None) #kwargs['filename']
        self.delimiter = kwargs.get('delimiter',None)
        self.encoding = kwargs.get('encoding',None)

    #Pass all the other names here if needed.

    def csv_loader(self):
        df = pd.read_csv(self.filepath)
        return df.values.tolist()

    def lazy_csv_loader(self):
        with open(self.filepath,'r',encoding=self.encoding) as csvfile:
            csvreader = csv.reader(csvfile,delimiter=self.delimiter)
            header = next(csvreader)
            yield header #yield is memory efficient

            for row in csvreader:
                yield row

if __name__ == "__main__":
    filedir = "../DATA"
    filename = "dataset_inventory_2018_03_11.csv"
    filepath = os.path.join(filedir,filename)
    loader = CSV_Loader(filepath=filepath,delimiter=",",encoding="utf-8")
    #print (loader.csv_loader())

    for row in loader.lazy_csv_loader():
        print (row)

