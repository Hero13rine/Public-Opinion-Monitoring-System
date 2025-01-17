from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config.default import Config

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # 从配置类加载配置
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    mail.init_app(app)

    # 配置日志
    import logging
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT']
    )

    # 注册路由
    from .routes import bp
    app.register_blueprint(bp)

    return app
