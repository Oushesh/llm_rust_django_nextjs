## Reference: https://colab.research.google.com/github/pinecone-io/examples/blob/master/learn/generation/llm-field-guide/open-llama/retrieval-augmentation-open-llama-langchain.ipynb#scrollTo=NTdsmU0AOZkL

from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type= "stuff",
    retriever=vectorstore.as_retriever(),
    reuturn_source_documents=True
)

result = qa(query)
#Result is of type dictionary
result["result"]