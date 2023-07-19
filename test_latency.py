# script to test gpt w and wo function 
from gpt import gpt_w_function, gpt
from extra.utils import load_prompt
from widgets.core import match_fn
from time import time
import random
import json

qs = ["What is the weather in SF?",
      "is it sunny in tokyo",
      "is it raining sao paolo",]

def log(**kwargs):
    with open('./latency.jsonl', 'a') as f:
        f.write(json.dumps(kwargs) + '\n')

def classifier(q):
    prompt = load_prompt('classifier')['prompt'].format(q=q, categories=match_fn.keys())
    ts = time()
    pred_widget_cls = gpt(prompt=prompt, max_tokens=2)["choices"][0]["message"]["content"]
    elapsed = time() - ts
    log(model='classifier', labels=pred_widget_cls, elapsed=elapsed)
    return pred_widget_cls

def extract_params(q): 
    prompt = load_prompt('extract_params')['weather']['prompt'].format(q=q)
    ts = time()
    pred_location = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    elapsed = time() - ts
    log(model='extract_params', labels=pred_location, elapsed=elapsed)

def fn_cls_and_extract(q): 
    categories = list(match_fn.keys())
    fns = [{
        "name": "get_current_weather",
        "description": "Get current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or zip code, e.g. San Francisco, CA"
                },
                "category": {
                    "type": "string",
                    "description": "Given a sentence, predict category",
                    "enum": categories 
                }
            },
            "required": ["location", "category"]
        }
    }] 
    prompt = load_prompt('fn')['prompt'].format(q=q)
    st = time()
    res = gpt_w_function(prompt=prompt, functions=fns)['choices'][0]['message']['function_call']['arguments']
    elapsed = time() - st
    model = 'fn'
    log(model=model, labels=res, elapsed=elapsed)
    return res

k = 20 
random.seed(42)
for q in random.choices(qs, k=k):
    fn_cls_and_extract(q)
    classifier(q)
    extract_params(q)