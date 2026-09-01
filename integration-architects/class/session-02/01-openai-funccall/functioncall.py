""""

pip install openai requests
"""


import os
import json
import requests
from openai import OpenAI

#     api_key="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",

client = OpenAI(
     api_key="<your api key>",
     base_url="https://llmgw-learn.tekstac.com"
     )


def get_weather(city: str) -> dict:
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

    result = dummy_weather.get(
        city,
        {
            "temperature": 25,
            "condition": "Unknown",
            "humidity": 60
        }
    )

    return {
        "city": city,
        **result
    }



def execute_tool(function_name: str, arguments: dict):
    if function_name == "get_weather":
        return get_weather(**arguments)



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

messages = [
    {
        "role": "system",
        "content": (
            "You are a professional agent. "
        )
    },
    {
        "role": "user",
        "content": "tell me weather of Pune city"
#        "content": "tell me a joke!"
    }
]

response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = messages,
    tools = tools,
    tool_choice = "auto"
)


assistant_message = response.choices[0].message

if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\n--------------------------------")
            print("LLM SELECTED TOOL")
            print("--------------------------------")
            print("Function :", function_name)
            print("Arguments:", arguments)

            # Execute Python function
            result = execute_tool(
                function_name,
                arguments
            )

            print("\nTOOL RESULT:")
            print(
                json.dumps(
                    result,
                    indent=2
                )
            )

else:
     print("No tool call detected")             


