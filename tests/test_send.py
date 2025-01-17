import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 配置 SMTP 信息
MAIL_SERVER = 'smtp.163.com'               # SMTP 服务器地址
MAIL_PORT = 465                            # SMTP 端口（SSL 使用 465，TLS 使用 587）
MAIL_USERNAME = 'liuzhikaisau@163.com'       # 你的邮箱地址
MAIL_PASSWORD = 'HKUwVx9AynykcyKh'           # 邮箱授权码
MAIL_RECIPIENT = 'herobrineLiu@outlook.com'   # 收件人邮箱

def send_email():
    """
    测试发送邮件
    """
    try:
        # 创建邮件内容
        subject = "SMTP 邮件发送测试"
        body = "这是一封测试邮件，证明 SMTP 邮件发送功能正常。"
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = Header(MAIL_USERNAME, 'utf-8')
        msg['To'] = Header(MAIL_RECIPIENT, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        # 连接到 SMTP 服务器并发送邮件
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as server:  # 使用 SSL 加密
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, [MAIL_RECIPIENT], msg.as_string())
            print("邮件发送成功！")

    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    send_email()
