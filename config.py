# config.py
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'iot-web-fuzz-secret-key'
    BOOFUZZ_WEB_PORT = 9000  # Boofuzz监控端口
    POC_DIR = "pocs"  # POC存储目录
    ALLOWED_EXTENSIONS = {'pcap', 'txt', 'har'}

    @staticmethod
    def init_app(app):
        # 创建必要目录
        for folder in [Config.POC_DIR]:
            os.makedirs(folder, exist_ok=True)