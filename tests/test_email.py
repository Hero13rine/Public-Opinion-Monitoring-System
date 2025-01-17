from flask import Flask
from app.services.email import send_alert_email
from config.default import Config

# 初始化 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化 Flask-Mail
from flask_mail import Mail
mail = Mail(app)

def test_send_alert_email():
    """
    测试发送敏感词检测警报邮件。
    """
    try:
        # 模拟测试数据
        sensitive_words = [
            {"word": "敏感词1", "level": "重大"},
            {"word": "敏感词2", "level": "特别重大"}
        ]
        weibo_text = "这是一条测试微博，包含敏感词1和敏感词2。"
        recipients = [Config.MAIL_DEFAULT_RECIPIENT]  # 替换为测试收件人邮箱

        # 发送邮件
        with app.app_context():
            send_alert_email(sensitive_words, weibo_text, recipients)

        print("测试邮件发送成功！")

    except Exception as e:
        print(f"测试邮件发送失败: {e}")

if __name__ == "__main__":
    test_send_alert_email()
