import os
import openai
import backoff
from extra.logger_config import setup_logger
import pprint
import json

logger = setup_logger(__name__)

from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

class RetriableError(Exception):
    pass

class FatalError(Exception):
    pass

retriable_exceptions = (openai.error.APIError, openai.error.Timeout, openai.error.RateLimitError)

def non_retriable(e):
    return not isinstance(e, retriable_exceptions)

def handle_success(d):
    l = { "elapsed": d['elapsed'], 
          "model_type": 'fn' if 'functions' in d['kwargs'] else 'compl'}
    with open('./latency.jsonl', 'a') as f:
        f.write(json.dumps(l) + '\n')
    pprint.pprint(d)

@backoff.on_exception(backoff.expo, openai.error.OpenAIError, max_tries=5, giveup=non_retriable, on_success=handle_success)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs, timeout=2)

def gpt(prompt, model="gpt-3.5-turbo-0613", temperature=0.5, max_tokens=1000, n=1, stop=None):
    messages = [{"role": "user", "content": prompt}]
    res = completions_with_backoff(messages=messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    return res

def gpt_w_function(prompt, functions, model="gpt-3.5-turbo-0613", temperature=0.5, max_tokens=1000, n=1, stop=None):
    messages = [{"role": "user", "content": prompt}]
    res = completions_with_backoff(messages=messages, functions=functions, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    return res
