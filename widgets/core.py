from . import core_bp
from gpt import gpt
from flask import jsonify, request
from extra.logger_config import setup_logger
from extra.utils import load_yaml

logger = setup_logger(__name__)

def handle_weather():
    return jsonify({'object': 'WeatherWidget', 'data': {}}), 200

def handle_calculator():
    return jsonify({'object': 'CalculatorWidget', 'data': {}}), 200

def handle_time():
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
    raw_prompt = load_yaml('./prompt/prompts.yaml')['widget_classifier']['prompt']
    prompt = raw_prompt.format(q=q, categories=match_fn.keys())
    pred_widget_cls = gpt(prompt=prompt)["choices"][0]["message"]["content"]
    return match_fn[pred_widget_cls]()