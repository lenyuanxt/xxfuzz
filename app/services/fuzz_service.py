import requests

def send_request_by_content(req):
    method = req.get('method', 'GET').upper()
    url = req.get('path', '')
    if not url.startswith('http'):
        url = 'http://127.0.0.1' + url
    headers = {}
    if isinstance(req.get('headers'), str):
        for line in req['headers'].split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                headers[k.strip()] = v.strip()
    else:
        headers = req.get('headers', {})
    cookies = {}
    if isinstance(req.get('cookies'), str):
        for pair in req['cookies'].split(';'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                cookies[k.strip()] = v.strip()
    else:
        cookies = req.get('cookies', {})
    params = {}
    if isinstance(req.get('query'), str):
        for pair in req['query'].split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k.strip()] = v.strip()
    else:
        params = req.get('query', {})
    body = req.get('body', '')
    try:
        ct = req.get('content_type', '') or headers.get('Content-Type', '')
        if ct.startswith('application/json'):
            import json as _json
            data = None
            json_data = None
            try:
                json_data = _json.loads(body) if body else {}
            except Exception:
                json_data = {}
            resp = requests.request(method, url, headers=headers, cookies=cookies, params=params, json=json_data, timeout=10)
        elif ct.startswith('application/x-www-form-urlencoded'):
            data = {}
            if body:
                for k, v in [item.split('=') for item in body.split('&') if '=' in item]:
                    data[k] = v
            resp = requests.request(method, url, headers=headers, cookies=cookies, params=params, data=data, timeout=10)
        else:
            resp = requests.request(method, url, headers=headers, cookies=cookies, params=params, data=body, timeout=10)
        return {'success': True, 'response': f'Status: {resp.status_code}\n' + resp.text}
    except Exception as e:
        return {'success': False, 'error': str(e)} 