import requests
import openai


class ApiManager:
    def __init__(self, model_name, api_key):
        self.api_endpoint = model_name
        openai.api_key = api_key

    def get_ai_response(self, message) -> str:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
        completion = openai.ChatCompletion.create(
            model=self.api_endpoint, messages=conversation
        )
        response_message = completion.choices[0].message
        return response_message
