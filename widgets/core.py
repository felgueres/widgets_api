from . import core_bp
from gpt import gpt
from flask import jsonify, request
from extra.logger_config import setup_logger
from extra.utils import load_prompt 

logger = setup_logger(__name__)

def handle_weather():
    # get fn params and call api
    return jsonify({'object': 'WeatherWidget', 'data': {}}), 200

def handle_calculator():
    # get fn params and evaluate expression 
    return jsonify({'object': 'CalculatorWidget', 'data': {}}), 200

def handle_time():
    # no need for params, just return current time
    return jsonify({'object': 'TimeWidget', 'data': {}}), 200

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
    return match_fn[pred_widget_cls]()
