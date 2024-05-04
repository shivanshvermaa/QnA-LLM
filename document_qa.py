import os
import yaml

from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI

import chainlit as cl
from chainlit.types import AskFileResponse

#Project configurations Configurations
with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

print(configs)

#OpenAPI configurations
os.environ["OPENAI_API_KEY"]=configs['openai']['api-key']

#This creates recurisve text splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#This gets the OpenAI Embeddings
embeddings = OpenAIEmbeddings()

welcome_message = """Welcome to the Chainlit PDF QA demo! To get started:
1. Upload a PDF or text file
2. Ask a question about the file
"""

def process_file(file):
    import tempfile

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        # tempfile.write(file.content)
        # print(type(file))
        loader = Loader(file.path)
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs


def get_docsearch(file : AskFileResponse):

    docs = process_file(file)

    cl.user_session.set("docs",docs)

    docsearch = Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )

    return docsearch

@cl.on_chat_start
async def start():

    await cl.Message(content="Start chatting with your PDFs.").send()

    files = None

    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain","application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    message = cl.Message(content=f"Processing {file.name}")
    await message.send()

    docsearh = await cl.make_async(get_docsearch)(file)
    print("Docsearch Completed")
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0,streaming=True),
        chain_type="stuff",
        retriever=docsearh.as_retriever(max_token_limit=4097)
    )

    message.content = f"{file.name} is done being processed"
    await message.update()

    cl.user_session.set("chain",chain)

@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,answer_prefix_tokens=["Final","git "]
    )
    cb.answer_reached = True
    response = await chain.acall(message.content,callbacks=[cb])

    answer = response["answer"]
    sources = response["sources"].strip()
    source_elements = []

    docs = cl.user_session.get("docs")
    metadatas = [doc.metadata for doc in docs]
    all_sources = [m["source"] for m in metadatas]

    if sources:
        found_sources = []

        # Add the sources to the message
        for source in sources.split(","):
            source_name = source.strip().replace(".", "")
            # Get the index of the source
            try:
                index = all_sources.index(source_name)
            except ValueError:
                continue
            text = docs[index].page_content
            found_sources.append(source_name)
            # Create the text element referenced in the message
            source_elements.append(cl.Text(content=text, name=source_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\nNo sources found"

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=source_elements).send()





