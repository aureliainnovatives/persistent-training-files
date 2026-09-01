""""
pip install langchain openai requests langchain-openai dotenv
"""


import os
import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()


MODEL = "openai:gpt-5.4"

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city from a demo weather service"""
    weather = {
        "nashik": "26 C, partly cloudy, humidity 68%",
        "pune": "24 C, rainy, humidity 78%",
        "mumbai": "29 C, cloudy, humidity 84%",
    }
    return weather.get(city.lower(), f"No demo weather data available for {city}.")



agent = create_agent(
    model = MODEL,
    tools = [
        get_weather
    ],
    system_prompt = (
        "You are an enterprise integration assistant. "
        "Choose tools only when they are useful. "
        "You may call more than one tool when the request has multiple parts. "
      
    )
)


def run(question: str) -> None:

    result = agent.invoke(
        {
            "messages": [
                {
                    "role":"user",
                    "content": question
                }
            ]
        }
    )

    print("\nFINAL ANSWER\n")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    print("Langchain Example :")


    while True:
        question = input("Enter a question: ")

        if question == "exit":
            break

        run(question)