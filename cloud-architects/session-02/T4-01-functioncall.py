"""
python -m venv venv

For MacOS or Linux:
    source venv/bin/activate

For Windows
    venv/Scripts/activate

pip install openai requests 
"""

import os
from openai import OpenAI
import requests
import json

def get_weather(city):

    dummy_weather = {
        "Nashik": {
            "temperature": 26,
            "condition": "Partly Cloudy",
            "humidity": 68
        },
        "Pune": {
            "temperature": 24,
            "condition": "Rainy",
            "humidity": 78
        },
        "Mumbai": {
            "temperature": 29,
            "condition": "Cloudy",
            "humidity": 84
        }
    }

    result = dummy_weather.get(city, {
        "temperature": 25,
        "condition": "Unknown",
        "humidity": 60
    })

    return {
        "city": city,
        **result
    }



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get current weather information for a city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name such as Pune or Mumbai"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
]

client = OpenAI(
        api_key="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"
    )




messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that answers questions based on the provided context."
    },
    {
        "role": "user",
#        "content": "what's the weather in Pune?"
        "content": "tell me history of Machine Learning"
    }
]

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = messages,
    tools = tools,
    tool_choice = "auto"
)

print(response)

if response.choices[0].message.tool_calls :

    for tool_call in response.choices[0].message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            if function_name == "get_weather":
                result = get_weather(arguments["city"])
                print("\n\n------ Function called : Get Weather ------ Result : ", result)

else:
    print("\n\n------ No Function Called ------")            
    print(response.choices[0].message.content)