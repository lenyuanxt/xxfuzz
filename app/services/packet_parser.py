import re
from urllib.parse import urlparse, parse_qs


class HTTPParser:
    def __init__(self, raw_packet):
        self.raw = raw_packet.strip()
        self.parsed = {
            'method': '',
            'url': '',
            'path': '',
            'query_params': {},
            'http_version': '',
            'headers': {},
            'cookies': {},
            'body': '',
            'body_params': {},
            'raw': raw_packet
        }

    def parse(self):
        """解析HTTP请求包"""
        lines = self.raw.split('\n')

        # 解析请求行
        request_line = lines[0].strip()
        method, url, http_version = self._parse_request_line(request_line)
        self.parsed['method'] = method
        self.parsed['url'] = url
        self.parsed['http_version'] = http_version

        # 解析URL和查询参数
        parsed_url = urlparse(url)
        self.parsed['path'] = parsed_url.path
        self.parsed['query_params'] = parse_qs(parsed_url.query)

        # 解析头部和cookie
        idx = 1
        for i, line in enumerate(lines[1:], start=1):
            line = line.strip()
            if not line:  # 空行表示头部结束
                idx = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                self.parsed['headers'][key] = value

                # 特殊处理Cookie
                if key.lower() == 'cookie':
                    self.parsed['cookies'] = self._parse_cookies(value)

        # 解析请求体
        body = '\n'.join(lines[idx:]).strip()
        self.parsed['body'] = body

        # 解析表单数据
        if body and 'Content-Type' in self.parsed['headers']:
            content_type = self.parsed['headers']['Content-Type']
            if 'application/x-www-form-urlencoded' in content_type:
                self.parsed['body_params'] = parse_qs(body)
            elif 'application/json' in content_type:
                try:
                    import json
                    self.parsed['body_params'] = json.loads(body)
                except:
                    pass  # 不是有效JSON则跳过

        return self.parsed

    def _parse_request_line(self, line):
        """解析请求行: GET /path?param=value HTTP/1.1"""
        match = re.match(r'^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(.*?)\s+(HTTP/\d\.\d)$', line)
        if match:
            return match.groups()
        return '', '', ''

    def _parse_cookies(self, cookie_str):
        """解析Cookie字符串"""
        cookies = {}
        for cookie in cookie_str.split(';'):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies

    def get_fuzzable_fields(self):
        """获取可模糊测试的字段"""
        return {
            'method': {'type': 'enum', 'values': ['GET', 'POST', 'PUT', 'DELETE']},
            'path': {'type': 'string'},
            'query_params': {param: {'type': 'string'} for param in self.parsed['query_params']},
            'headers': {header: {'type': 'string'} for header in self.parsed['headers'] if
                        header.lower() not in ['host', 'content-length']},
            'cookies': {cookie: {'type': 'string'} for cookie in self.parsed['cookies']},
            'body': {'type': 'string'}
        }