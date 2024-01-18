from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, ConversableAgent
from decouple import config
import chainlit as cl


def chat_new_message(self, message, sender):
    cl.run_sync(
        cl.Message(
            content="",
            author=sender.name,
        ).send()
    )
    content = message
    cl.run_sync(
        cl.Message(
            content=content,
            author=sender.name,
        ).send()
    )


def config_personas():
    config_list = [{
        "model": "gpt-3.5-turbo-1106",  # model name
        "api_key": config("OPENAI_API_KEY")  # api key
    }]

    llm_config = {
        "seed": 14,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0.7,  # temperature for sampling
    }

    user_proxy = UserProxyAgent(
        name="Admin",
        system_message="A human admin. Interact with the planner to discuss the plan. "
                       "Plan execution needs to be approved by this admin.",
        code_execution_config=False,
        max_consecutive_auto_reply=10,
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    developer = AssistantAgent(
        name="Developer",
        system_message='''Developer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the 
        code in a code block that specifies the script type. The user can't modify your code. So do not suggest 
        incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by 
        the Quality_Assurance. Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. 
        Check the execution result returned by the Quality_Assurance. If the result indicates there is an error, fix the error and 
        output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed 
        or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your 
        assumption, collect additional info you need, and think of a different approach to try.''',
        llm_config=llm_config
    )

    scrum_master = AssistantAgent(
        name="Scrum_Master",
        system_message='''Scrum_Master. Suggest a plan. Revise the plan based on feedback from admin and Product_Owner, until admin 
        approval. The plan may involve an Developer who can write code and an Quality_Assurance and Product_Owner who doesn't write code. 
        Explain the plan first. Be clear which step is performed by a Developer, Quality_Assurance, and Product_Owner.''',
        llm_config=llm_config
    )

    quality_assurance = AssistantAgent(
        name="Quality_Assurance",
        system_message="Quality_Assurance. Execute the code written by the Developer and report the result.",
        code_execution_config={"last_n_messages": 3, "work_dir": "feedback"},
        llm_config=llm_config
    )

    product_owner = AssistantAgent(
        name="ProductOwner",
        system_message="Product_Owner. Double check plan, claims, code from other agents and provide feedback.",
        llm_config=llm_config
    )

    group_chat = GroupChat(
        agents=[user_proxy, developer, scrum_master,
                quality_assurance, product_owner], messages=[], max_round=50
    )
    
    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    return user_proxy, manager


def start_chat_saas(message, is_test=False):
    if not is_test:
        ConversableAgent._print_received_message = chat_new_message
    user_proxy, manager = config_personas()
    user_proxy.initiate_chat(manager, message=message)


if __name__ == "__main__":
    test_message = (
        "I would like to build a simple website that collects feedback from "
        "consumers via forms.  We can just use a flask application that creates an "
        "html website with forms and has a single question if they liked their "
        "customer experience and then keeps that answer.  I need a thank you html "
        "page once they completed the survey.  I then need a html page called "
        "admin that gives a nice table layout of all of the records from the "
        "database.  Just use sqlite3 as the database, keep it simple.  Also use "
        "Bootstrap for the CSS Styling.")
    start_chat_saas(test_message, is_test=True)
