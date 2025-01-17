import logging

class Config:
    # 添加邮箱smtp服务密钥
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '*********'
    MAIL_PASSWORD = '*********'
    MAIL_DEFAULT_SENDER = '*********'
    MAIL_DEFAULT_RECIPIENT = '*********'
    # 添加数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3308/weibo_analysis'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    THRESHOLD = "较大"  # 默认阈值
    # 日志配置
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

