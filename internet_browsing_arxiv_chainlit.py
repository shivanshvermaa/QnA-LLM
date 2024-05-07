import os
import yaml

from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

import chainlit as cl


#Project configurations Configurations
with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

# print(configs)

#OpenAPI configurations
os.environ["OPENAI_API_KEY"]=configs['openai']['api-key']


@cl.on_chat_start
def start():
    llm = ChatOpenAI(
        streaming = True
    )

    tools = load_tools(
        ["arxiv"]
    )

    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose = True,
        handle_parsing_errors = True
    )

    cl.user_session.set("agent",agent_chain)

@cl.on_message
async def main(message):

    agent = cl.user_session.get("agent")

    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.run)(message.content, callbacks=[cb])
