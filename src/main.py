import chainlit as cl

from saas import start_chat_saas
from script import start_chat_script
from genocs_dev import start_chat_genocs_dev


@cl.set_chat_profiles
async def set_chat_profile():
    return [
        cl.ChatProfile(
            name="YouTube Scriptwriting",
            markdown_description="Your next YouTube video script is just a few messages away!",
        ),
        cl.ChatProfile(
            name="Awesome Startup",
            markdown_description="Get your next SaaS product idea in a few messages!",
        ),
        cl.ChatProfile(
            name="Genocs Developer",
            markdown_description="Build your awesome product by means of Genocs .NET library!",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"Welcome to {chat_profile} chat. Please type your first message to get started."
    ).send()


@cl.on_message
async def on_message(message):
    chat_profile = cl.user_session.get("chat_profile")
    message_content = message.content
    if chat_profile == "YouTube Scriptwriting":
        start_chat_script(message_content)
    elif chat_profile == "Awesome Startup":
        start_chat_saas(message_content)
    elif chat_profile == "Genocs Developer":
        start_chat_genocs_dev(message_content)
