import pinecone
import openai

from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

from langchain.embeddings import OpenAIEmbeddings
load_dotenv() #load_dotenv to load all .env variables

embeddings = OpenAIEmbeddings()
text = "Algorithm is a data science school based in Indonesia"
doc_embeddings = embeddings.embed_documents([text])

print (doc_embeddings)

index = pinecone.Index('nietzsche')

# Initialize OpenAI
openai.api_key =


#Talk to your documents.
"""
dburi = "sqlite:///academy/academy.db"
db = SQLDatabase.from_url(dburi)
llm = OpenAI(temperature=0)

db_chain = SQLDatabaseChain(llm=llm,database=db,verbose=True)

db_chain.run("How many rows is in the responses table of this db?")
db_chain.run("Describe the response table")
db_chain.run("What are the top 3 countries where those are from?")
db_chain.run("Give me a summary of how these customers came to hear about us. What is the most common way they hear about it?")
"""

#move the sql to supabase in the future:

#Add Data module and
