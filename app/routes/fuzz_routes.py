from flask import Blueprint, render_template, request, jsonify
from app.services.fuzz_service import send_request_by_content

bp = Blueprint('fuzz', __name__, url_prefix='/fuzz')

@bp.route('/', methods=['GET'])
def fuzz_page():
    return render_template('fuzz.html')

@bp.route('/send', methods=['POST'])
def fuzz_send():
    data = request.get_json()
    req = data.get('request')
    if not req:
        return jsonify({'success': False, 'error': '未提供请求内容'})
    result = send_request_by_content(req)
    return jsonify(result) 