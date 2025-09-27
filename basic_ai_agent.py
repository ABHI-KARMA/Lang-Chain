import requests
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

import os
os.environ["OPENAI_API_KEY"] = "Your-OPENAI-API-KEY"
WEATHER_API_KEY = "key"

# Initializing the duckduckgosearch tool
search_tool = DuckDuckGoSearchRun()

# Creating custom tool using decorator "@tool"
# we have to mention that, what is this tool using for within the function, also perfactly give the needed parameter in similary way
@tool
def get_weather_data(city: str) -> str:
	"""
		This function fetches the current weather data for a given city
	"""
	url = f'https://api.weatherstack.com/current?access_key={WEATHER_API_KEY}={city}'
	response = requests.get(url)
	return response.json()

# Initializing llm model
llm = ChatOpenAI()

# pull the standard ReAct agent prompt
prompt = hub.pull("hwchase17/react")

# create the ReAct agent manually with pulled prompt and tools
agent = create_react_agent(
		llm=llm,
		tools=[get_weather_data,search_tool],
		prompt=prompt
	)

# create the agent Executor
agent_executor = AgentExecutor(
		agent=agent,
		tools=[get_weather_data,search_tool],
		verbose=True
	)

while True:
	request = input("Enter your question or exit :- ")
	if request in ['q','exit','leave']:
		break

	# Invoke the Executor
	response = agent_executor.invoke({"input": request})
	print(response['output'])
