## This script allows to store and query the embeddings from PineCone.

from langchain.vectorstores import Pinecone

text_field = "text"

# switch back to normal index for langchain
index = pinecone.Index(index_name)

vectorstore = Pinecone(
    index,embed.embed_query,text_field
)

query = "Do I need to get my pet tested for COVID-19?"

vectorstore.similarity_search(
    query, #our search query
    k=3    # return 3 most relevant docs
)