from . import core_bp
from gpt import gpt
from flask import jsonify, request
from extra.logger_config import setup_logger
from extra.utils import load_yaml

logger = setup_logger(__name__)

widget_cls = {
    'weather': handle_weather,
    'calculator': handle_calculator,
    'time': handle_time,
}

def handle_weather():
    return jsonify({'object': 'CurrentWeather', 'data': {}}), 200

def handle_calculator():
    return jsonify({'object': 'Calculator', 'data': {}}), 200

def handle_time():
    return jsonify({'object': 'Time', 'data': {}}), 200

@core_bp.route('/v1/search', methods=['POST'])
def search():
    q = request.args.get('q')
    cls_prompt = load_yaml('./prompt/prompts.yaml')['widget_classifier']['prompt'].format(q=q)
    widget_category = gpt(prompt=cls_prompt)
    if widget_category in widget_cls:
        return widget_cls[widget_category]()
    return jsonify({'object': 'SearchResult', 'data': {}}), 200
