"""Python file to serve as the frontend"""
import sys
import os

from langchain import OpenAI
from langchain.agents import create_csv_agent
from chainlit import user_session
import chainlit as cl

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

    llm = OpenAI(temperature=0, model_name=MODEL_NAME)
    csv_agent = create_csv_agent(llm=llm, path='/home/appuser/app/src/titanic.csv', verbose=True)

    return csv_agent
