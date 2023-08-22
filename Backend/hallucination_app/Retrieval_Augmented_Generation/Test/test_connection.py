import pinecone
import openai
import pandas as pd
import os
from dotenv import load_dotenv
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents.agent_types import AgentType
#from Backend.hallucination_app.Retrieval_Augmented_Generation.DATA

load_dotenv() #load_dotenv to load all .env variables

pinecone.init(
    api_key='33a06231-2b74-4529-8fe3-2c31717dd31c',
    environment='asia-southeast1-gcp-free'
)
index = pinecone.Index('nietzsche')

## Modify this part of the code and write my own agent.
## temperature 0 means deterministic.

from langchain.agents import create_csv_agent

base_dir = "../DATA"
filename = "dataset_inventory_2018_03_11.csv"

filepath = os.path.join(base_dir,filename)
loader = CSVLoader(filepath)
print (loader)

#Goal: Build a personal agent from LLMAAPI, path of data

agent = create_csv_agent(
    OpenAI(temperature=0),
    filepath,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent.run("How many rows are there in this csv?")
agent.run("What is this document about?")
#agent.run("What percentage of the respondents are students versus professionals?")
#agent.run("List the top 3 devices that the respondents use to submit their responses")
#agent.run("Consider iOS and Android as mobile devices. What is the percentage of respondents that discovered us through social media submitting this from a mobile device?")

#move documents to supabase --> then perform the AI Embedding

#Pre Embed The Documents on Supabase