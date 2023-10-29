"""Python file to serve as the frontend"""
import sys
import os

from langchain.llms import OpenAI
import chainlit as cl
from chainlit import user_session

from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader

sys.path.append(os.path.abspath('.'))

# user_env = user_session.get("env")
MODEL_NAME = "text-davinci-003"

TEMPLATE = """Question: {question}

Answer: Let's think step by step."""

@cl.langchain_factory(use_async=True)
def factory():
    """ The langchain factory is a function that returns a chain instance.
    """

    user_env = cl.user_session.get("env")
    os.environ["OPENAI_API_KEY"] = user_env.get("OPENAI_API_KEY")
    # Instantiate the chain for that user session
    # prompt = PromptTemplate(template=TEMPLATE, input_variables=["question"])

    # llm = OpenAI(temperature=0, model_name=MODEL_NAME)
    # csv_agent = create_csv_agent(llm=llm, path='src/titanic.csv', verbose=True)

    loader = TextLoader('src/company_description.txt')
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(texts, embeddings)

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vectordb.as_retriever())

    return qa
