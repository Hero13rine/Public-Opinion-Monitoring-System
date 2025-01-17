from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 配置全局变量（例如：阈值设置）
app.config['THRESHOLD'] = "重大"  # 默认预警等级

# 路由：主页
@app.route('/')
def index():
    # 模拟分析结果数据
    results = [
        {"id": 1, "text": "这是一条测试评论", "sensitive_words": ["测试", "敏感"], "alert_level": "低", "created_at": "2025-01-17"},
        {"id": 2, "text": "另一条重要评论", "sensitive_words": ["重要"], "alert_level": "重大", "created_at": "2025-01-16"},
    ]
    return render_template('dashboard.html', results=results, threshold=app.config['THRESHOLD'])

# 路由：设置阈值
@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    new_threshold = request.form['threshold']
    app.config['THRESHOLD'] = new_threshold
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)