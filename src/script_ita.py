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
        name="User_Proxy",
        system_message="L'amministratore.",
        max_consecutive_auto_reply=10,
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    content_creator = AssistantAgent(
        name="Content_Creator",
        system_message='''Sono il creatore di contenuti che prepara discorsi riguardanti argomenti scientifici relativi alle Biotecnologie. 
        Vorrei creare una interessante e accattivante presentazione per il mio pubblico riguardo le ultime notità relative alle Biotecnologie. 
        Vorrei fornire informazioni dettagliate utilizzando le maggiori riviste scientifiche che parlano di Biotecnologie.''',
        llm_config=llm_config
    )

    script_writer = AssistantAgent(
        name="Script_Writer",
        system_message='''Io sono lo scrittore per il Creatore di Contenuti.  Devo scrivere un discorso fluido tale da poter essere esposto eloquentemente
        dal creatore di contenuti riguardo le Biotecnologie.''',
        llm_config=llm_config
    )

    researcher = AssistantAgent(
        name="Researcher",
        system_message='''Io sono il Ricercatore che lavoro per conto del Creatore di Contenuti e cerco le ultime novità nelle pubblicazioni scientifiche riguardanti le Biotecnologie. 
        Nei miei riferimenti includo sempre: il titolo dell'articolo, il nome della rivista e l'anno di pubblicazione tra le informazioni da consegnare al Script_Writer.''',
        llm_config=llm_config
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        system_message='''Io sono il Revisore del Creatore di Contenuti e del Ricercatore, una volta finito il loro lavoro di stesure del documento. 
        Io controllo il risultato e do i miei consigli e suggerimenti.''',
        llm_config=llm_config
    )

    group_chat = GroupChat(
        agents=[user_proxy, content_creator, script_writer,
                researcher, reviewer], messages=[]
    )
    
    manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

    return user_proxy, manager


def start_chat_script_ita(message, is_test=False):
    if not is_test:
        ConversableAgent._print_received_message = chat_new_message
    user_proxy, manager = config_personas()
    user_proxy.initiate_chat(manager, message=message)


if __name__ == "__main__":
    test_message = ("I need to create a YouTube Script that talks about the latest paper about gpt-4 on arxiv and its "
                    "potential applications in software.")
    start_chat_script_ita(test_message, is_test=True)
