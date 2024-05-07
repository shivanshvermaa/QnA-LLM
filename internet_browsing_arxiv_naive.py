import os
import yaml

from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import ChatOpenAI


#Project configurations Configurations
with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

print(configs)

#OpenAPI configurations
os.environ["OPENAI_API_KEY"]=configs['openai']['api-key']

llm = ChatOpenAI(temperature=0.3)
tools = load_tools(
    ["arxiv"]
)

agent_chain = initialize_agent(
    tools=tools,
    llm = llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent_chain.run("What is RLHF for Large Language Models")