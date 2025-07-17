# app/__init__.py
from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化配置
    config_class.init_app(app)

    # 注册蓝图
    from app.routes.main_routes import bp as main_bp
    from app.routes.packet_routes import bp as packet_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(packet_bp)  # 添加数据包路由

    return app