import pytest
from hai.utils.chat_price import (
    GPT_4_PRICE_PER_TOKEN,
    num_tokens_from_messages_openai,
    num_tokens_from_completion_openai,
    price_for_completion,
    gpt_pricing,
    PriceChatListener,
)


def test_num_tokens_from_messages_openai():
    message = [{"role": "user", "content": "Hello GPT!"}]
    model = "gpt-4"
    assert num_tokens_from_messages_openai(message, model) == 11


def test_num_tokens_from_completion_openai():
    completion = {"role": "assistant", "content": "Hello user!"}
    model = "gpt-4"
    assert num_tokens_from_completion_openai(completion, model) == 10


def test_price_for_completion():
    messages = [{"role": "user", "content": "Hello GPT!"}]
    response = {"role": "assistant", "content": "Hello user!"}
    model = "gpt-4"
    assert (
        price_for_completion(messages, response, model) == 0.0009299999999999999
    )


def test_gpt_pricing():
    model = "gpt-4"
    assert gpt_pricing(model, True) == GPT_4_PRICE_PER_TOKEN["prompt"]


def test_PriceChatListener():
    listener = PriceChatListener()

    messages = [{"role": "user", "content": "Hello GPT!"}]
    response = {"role": "assistant", "content": "Hello user!"}
    model = "gpt-4"

    listener.on_chat_response(messages, response, model)
    assert listener.current_spend == 0.0009299999999999999
