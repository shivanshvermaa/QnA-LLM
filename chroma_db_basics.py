import chromadb

chroma_client = chromadb.Client()

#Creating a collection which is as equivalent as a
collection = chroma_client.create_collection(name = "my_collection")

collection.add(
    documents = ["my name is shivansh","my name is not shivansh"],
    metadatas = [{
        "source" : "my name is true"
    },
    {
        "source" : "my name is false"
    }],
    ids = ["id1","id2 "]
)

result = collection.query(
    query_texts="What is my name",
    n_results=1
)

print(result)