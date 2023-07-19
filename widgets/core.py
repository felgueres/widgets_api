from . import core_bp
from gpt import gpt
from flask import jsonify, request
from .helpers import evaluate, get_current_time_in_tz, get_current_weather
from extra.logger_config import setup_logger
from extra.utils import load_prompt 

logger = setup_logger(__name__)

def handle_weather(q, metadata=None):
    prompt = load_prompt('extract_params')['weather']['prompt'].format(q=q)
    pred_location = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    cur_weather_data = get_current_weather(pred_location) 
    return jsonify({'object': 'WeatherWidget', 'data': cur_weather_data}), 200

def handle_calculator(q, metadata=None):
    prompt = load_prompt('extract_params')['calculator']['prompt'].format(q=q)
    pred_expr = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return jsonify({'object': 'CalculatorWidget', 'data': {'result': evaluate(pred_expr), 'expr': pred_expr}}), 200

def handle_time(q, metadata=None):
    prompt = load_prompt('extract_params')['time']['prompt'].format(q=q)
    pred_tz = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    if pred_tz == 'locale': pred_tz = 'America/Los_Angeles' #TODO: get locale from request
    current_time = get_current_time_in_tz(pred_tz)
    return jsonify({'object': 'TimeWidget', 'data': { 'time': current_time, 'tz': pred_tz}}), 200

match_fn = {
    'weather': handle_weather,
    'calculator': handle_calculator,
    'time': handle_time,
    'none': lambda: jsonify({'object': '', 'data': {}})
}

@core_bp.route('/v1/search', methods=['POST'])
def search():
    q = request.args.get('q')
    prompt = load_prompt('classifier')['prompt'].format(q=q, categories=match_fn.keys())
    pred_widget_cls = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return match_fn[pred_widget_cls](q)
