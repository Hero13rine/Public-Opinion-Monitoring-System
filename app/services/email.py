from flask_mail import Mail, Message
from flask import current_app
import logging
import json

# 初始化 Flask-Mail
mail = Mail()


def send_alert_email(sensitive_words, weibo_text, username, url, recipients=None):
    """
    发送敏感词检测警报邮件。

    参数:
        sensitive_words (list): 检测到的敏感词及其危险等级。
        weibo_text (str): 被检测的微博内容。
        recipients (list): 收件人邮箱列表，默认为 None 时发送到配置文件中的默认收件人。
    """
    try:
        # 使用 Flask 当前应用上下文发送邮件
        with current_app.app_context():
            # 默认收件人
            if not recipients:
                recipients = [current_app.config.get("MAIL_DEFAULT_SENDER")]

            # 生成敏感词详情
            sensitive_words_list = "\n".join(
                [f"- {word['word']} (等级: {word['level']})" for word in sensitive_words])
            # 创建邮件内容
            subject = "敏感词检测警报"
            body = (
                f"检测到敏感词：\n\n"
                f"微博内容: {weibo_text}\n\n"
                f"用户名: {username}\n\n"
                f"微博链接: {url}\n\n"
                f"敏感词详情:\n"
                f"{sensitive_words_list}\n\n"
                f"请及时处理！"
            )

            msg = Message(
                subject=subject,
                recipients=recipients
            )
            msg.body = body

            # 发送邮件
            mail.send(msg)
            logging.info(f"邮件已发送至: {', '.join(recipients)}")

    except Exception as e:
        logging.error(f"发送邮件失败: {e}")
        raise e