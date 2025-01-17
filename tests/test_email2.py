import smtplib

try:
    server = smtplib.SMTP_SSL('smtp.163.com', 465)  # SSL 方式
    server.login('liuzhikaisau@163.com', 'HKUwVx9AynykcyKh')
    print("连接成功，登录成功！")
    server.quit()
except Exception as e:
    print(f"连接失败: {e}")
