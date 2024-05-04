import chainlit as cl
# from openai import OpenAI
import os
import yaml
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain

#Project configurations Configurations
with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

print(configs)

#OpenAPI configurations
os.environ["OPENAI_API_KEY"]=configs['openai']['api-key']
# client = OpenAI()

template = """ Question : {question}
Answer : 
"""

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables = ["question"])
    llm_chain = LLMChain(prompt = prompt,llm=OpenAI(temperature=0,streaming=True),verbose=True)
#
    cl.user_session.set("llm_chain",llm_chain)

@cl.on_message
async def main(message ):
    llm_chain = cl.user_session.get("llm_chain")

    res = await llm_chain.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(content=res["text"]).send()