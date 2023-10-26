"""Python file to serve as the frontend"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.agents import create_csv_agent
import chainlit as cl

from chainlit import user_session

user_env = user_session.get("env")
model_name = "text-davinci-003"


# os.environ["OPENAI_API_KEY"] = ""

template = """Question: {question}

Answer: Let's think step by step."""

@cl.langchain_factory(use_async=True)
def factory():
    user_env = cl.user_session.get("env")
    os.environ["OPENAI_API_KEY"] = user_env.get("OPENAI_API_KEY")
    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = OpenAI(temperature=0, model_name=model_name)
    csv_agent = create_csv_agent(llm=llm, path='/home/appuser/app/src/titanic.csv', verbose=True)

    return csv_agent 

