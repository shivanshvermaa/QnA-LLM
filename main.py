import chainlit as cl
from openai import OpenAI
import yaml
import os


#Project configurations Configurations
with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

print(configs)

#OpenAPI configurations
os.environ["OPENAI_API_KEY"]=configs['openai']['api-key']
client = OpenAI()

messages = [{
                "role" : "system",
                "content" : "You are a helpful assistant!"
            }]
@cl.on_message
async def main(message):
    print(type(message))
    print(f"This is the message : {message.content}")
    messages.append(
        {
            "role": "user",
            "content": message.content
        }
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1
    )

    messages.append(
        {
            "role" : "assistant",
            "content" : response.choices[0].message.content
        }
    )

    await cl.Message(content = response.choices[0].message.content).send()