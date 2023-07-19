# script to test gpt w and wo function 
from gpt import gpt_w_function, gpt
from extra.utils import load_prompt
from widgets.core import match_fn

q = "What is the weather in SF?"

def classifier(q):
    prompt = load_prompt('classifier')['prompt'].format(q=q, categories=match_fn.keys())
    pred_widget_cls = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return pred_widget_cls

def extract(q):
    prompt = load_prompt('extract_params')['weather']['prompt'].format(q=q)
    pred_location = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return pred_location

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
    res = gpt_w_function(prompt=prompt, functions=fns)['choices'][0]['message']['function_call']['arguments']
    return res

n_tries = 10
for i in range(n_tries): 
    fn_cls_and_extract(q)
    classifier(q)


