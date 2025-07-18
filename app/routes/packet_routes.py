from flask import Blueprint, request, jsonify, render_template, send_from_directory
from app.services.packet_parser import HTTPParser

bp = Blueprint('packet', __name__, url_prefix='/packet')


@bp.route('/analyzer', methods=['GET'])
def analyzer_view():
    """数据包分析器页面"""
    return render_template('packet_analyzer.html')


@bp.route('/parse', methods=['POST'])
def parse_packet():
    """解析HTTP数据包"""
    raw_packet = request.form.get('raw_packet', '')
    if not raw_packet:
        return jsonify({'error': 'No packet provided'}), 400

    parser = HTTPParser(raw_packet)
    try:
        parsed_data = parser.parse()
        return jsonify({
            'success': True,
            'parsed': parsed_data,
            'fuzzable': parser.get_fuzzable_fields()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/save_template', methods=['POST'])
def save_template():
    """保存模板接口"""
    import os, json, time, re
    data = request.get_json()
    template = data.get('template')
    filename = data.get('filename')
    if not template:
        return jsonify({'success': False, 'error': 'No template data'}), 400
    save_dir = os.path.join(os.path.dirname(__file__), '../../uploads')
    os.makedirs(save_dir, exist_ok=True)
    # 文件名安全校验
    if filename:
        filename = filename.strip()
        # 只允许字母数字下划线中划线点，必须以.json结尾
        if not re.match(r'^[\w\-.]+\.json$', filename):
            return jsonify({'success': False, 'error': '文件名不合法，仅支持字母数字下划线中划线点且以.json结尾'}), 400
    else:
        ts = int(time.time())
        filename = f'template_{ts}.json'
    save_path = os.path.join(save_dir, filename)
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/list_templates', methods=['GET'])
def list_templates():
    """列出所有模板文件"""
    import os
    dir_path = os.path.join(os.path.dirname(__file__), '../../uploads')
    files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
    return jsonify({'success': True, 'templates': files})

@bp.route('/get_template/<filename>', methods=['GET'])
def get_template(filename):
    """获取单个模板内容"""
    import os, json
    dir_path = os.path.join(os.path.dirname(__file__), '../../uploads')
    file_path = os.path.join(dir_path, filename)
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': '模板不存在'}), 404
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify({'success': True, 'template': data})

@bp.route('/update_template/<filename>', methods=['POST'])
def update_template(filename):
    """保存（覆盖）模板内容"""
    import os, json
    dir_path = os.path.join(os.path.dirname(__file__), '../../uploads')
    file_path = os.path.join(dir_path, filename)
    data = request.get_json()
    template = data.get('template')
    if not template:
        return jsonify({'success': False, 'error': '无模板数据'}), 400
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    return jsonify({'success': True})

@bp.route('/delete_template/<filename>', methods=['POST'])
def delete_template(filename):
    """删除模板文件"""
    import os
    dir_path = os.path.join(os.path.dirname(__file__), '../../uploads')
    file_path = os.path.join(dir_path, filename)
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': '模板不存在'}), 404
    os.remove(file_path)
    return jsonify({'success': True})