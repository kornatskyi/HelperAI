from typing import Optional, TypedDict
import tiktoken

from hai.model.message import Message


class PriceChatListener:
    def __init__(self):
        self.current_spend = 0

    def on_chat_response(
        self, messages: list[Message], response: Message, model: str
    ):
        num_tokens = num_tokens_from_messages_openai(
            [*messages, response], model
        )
        price = price_for_completion(messages, response, model)
        self.current_spend += price
        print(
            f"Number of tokens in the last response + request: {int(num_tokens)}"
        )
        print(f"Current spend: ${self.current_spend:.3}")


GPT_3_5_TURBO_PRICE_PER_TOKEN = {
    "prompt": 0.0015 / 1000,
    "response": 0.002 / 1000,
}

GPT_3_5_TURBO_16K_PRICE_PER_TOKEN = {
    "prompt": 0.003 / 1000,
    "response": 0.004 / 1000,
}

GPT_4_PRICE_PER_TOKEN = {
    "prompt": 0.03 / 1000,
    "response": 0.06 / 1000,
}

GPT_4_32K_PRICE_PER_TOKEN = {
    "prompt": 0.06 / 1000,
    "response": 0.12 / 1000,
}


def gpt_pricing(model: str, prompt: bool) -> Optional[float]:
    if model.startswith("gpt-3.5-turbo-16k"):
        pricing = GPT_3_5_TURBO_16K_PRICE_PER_TOKEN
    elif model.startswith("gpt-3.5-turbo"):
        pricing = GPT_3_5_TURBO_PRICE_PER_TOKEN
    elif model.startswith("gpt-4-32k"):
        pricing = GPT_4_32K_PRICE_PER_TOKEN
    elif model.startswith("gpt-4"):
        pricing = GPT_4_PRICE_PER_TOKEN
    else:
        return None
    return pricing["prompt" if prompt else "response"]


def price_for_completion(
    messages: list[Message], response: Message, model: str
):
    num_tokens_prompt = num_tokens_from_messages_openai(messages, model)
    num_tokens_response = num_tokens_from_completion_openai(response, model)

    price_per_token_prompt = gpt_pricing(model, True)
    price_per_token_response = gpt_pricing(model, False)

    return (
        price_per_token_prompt * num_tokens_prompt
        + price_per_token_response * num_tokens_response
    )


def num_tokens_from_messages_openai(messages: list[Message], model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            assert isinstance(value, str)
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


def num_tokens_from_completion_openai(completion: Message, model: str) -> int:
    return num_tokens_from_messages_openai([completion], model)
