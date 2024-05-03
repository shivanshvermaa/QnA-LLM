import chainlit as cl
import openai
import yaml

with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

print(configs)

@cl.on_message
async def main(message : str):
    await cl.Message(content = message).send()