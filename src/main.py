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

class SingletonVerctorStore(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonVerctorStore, cls).__new__(cls)
            cls.load_document(cls.instance)
        return cls.instance
  
    def load_document(self) :
        print("Loading document...")
        loader = TextLoader('src/company_description.txt')
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        self.vectordb = Chroma.from_documents(texts, embeddings)
  

def get_qna() :
    """Get the qna agent for the company description"""
    
    # Use sigleton to load the document only once
    singleton = SingletonVerctorStore()
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=singleton.vectordb.as_retriever())
    return qa

def get_csv() :
    """Get the csv agent for the titanic.csv dataset"""
    # Instantiate the chain for that user session
    # prompt = PromptTemplate(template=TEMPLATE, input_variables=["question"])

    llm = OpenAI(temperature=0, model_name=MODEL_NAME)
    csv_agent = create_csv_agent(llm=llm, path='src/titanic.csv', verbose=True)
    return csv_agent


TEMPLATE = """Question: {question}


Answer: Let's think step by step."""

@cl.langchain_factory(use_async=True)
def factory():
    """ The langchain factory is a function that returns a chain instance.
    """

    user_env = cl.user_session.get("env")
    os.environ["OPENAI_API_KEY"] = user_env.get("OPENAI_API_KEY")

    # return get_csv()

    return get_qna()
