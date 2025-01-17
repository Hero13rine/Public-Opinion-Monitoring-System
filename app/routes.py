from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from .models import db, WeiboComment, AnalysisResult
from .services.spider import Spider
from .services.evaluation import evaluate_weibo_content
from .services.email import handle_alert
import re
from sqlalchemy import func
from threading import Event
from time import sleep
import json
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    # 查询分析结果
    results = AnalysisResult.query.join(WeiboComment).all()
    threshold = current_app.config.get('THRESHOLD', '重大')
    return render_template('dashboard.html', results=results, threshold=threshold)

@bp.route('/analyze', methods=['POST'])
def analyze_comments():
    # 获取用户提交的评论内容
    weibo_text = request.form.get('text')
    if not weibo_text:
        return "评论内容不能为空", 400

    # 保存评论到数据库
    weibo_comment = WeiboComment(
        weibo_id='generated_id',  # 假设生成微博ID
        text=weibo_text,
        url='https://weibo.com/example',  # 默认测试URL
        username='测试用户'  # 默认测试用户名
    )
    db.session.add(weibo_comment)
    db.session.commit()

    # 调用敏感词分析
    sensitive_words = evaluate_weibo_content(weibo_text)

    # 确定危险等级
    alert_level = max((word['level'] for word in sensitive_words), default='常态')

    # 保存分析结果
    analysis_result = AnalysisResult(
        comment_id=weibo_comment.id,
        sensitive_words=sensitive_words,
        alert_level=alert_level
    )
    db.session.add(analysis_result)
    db.session.commit()

    # 获取阈值并判断是否发送邮件
    handle_alert(alert_level, sensitive_words, weibo_comment, current_app)

    return redirect(url_for('routes.index'))

@bp.route('/set_threshold', methods=['POST'])
def set_threshold():
    new_threshold = request.form['threshold']
    current_app.config['THRESHOLD'] = new_threshold

    # 更新 config/default.py 文件
    config_file_path = 'config/default.py'
    with open(config_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式更新配置
    new_content = re.sub(
        r'THRESHOLD\s*=\s*".*?"',  # 匹配 THRESHOLD 的赋值语句
        f'THRESHOLD = "{new_threshold}"',  # 替换为新的阈值
        content
    )

    with open(config_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return redirect(url_for('routes.index'))


@bp.route('/fetch_comments')
def fetch_comments():
    spider = Spider()
    comments = spider.fetch_comments()  # 获取爬取结果

    for comment in comments:
        # 保存爬取的微博内容
        weibo_comment = WeiboComment(
            weibo_id=comment['url'].split('/')[-1],  # 假设从 URL 提取微博 ID
            text=comment['text'],
            url=comment['url'],
            username=comment['username'],
            created_at=comment['created_at']
        )

        db.session.add(weibo_comment)
        db.session.commit()

        # 调用敏感词分析
        sensitive_words = evaluate_weibo_content(comment['text'])

        # 确定危险等级
        alert_level = max((word['level'] for word in sensitive_words), default='常态')

        # 保存分析结果
        analysis_result = AnalysisResult(
            comment_id=weibo_comment.id,
            sensitive_words=sensitive_words,
            alert_level=alert_level
        )
        db.session.add(analysis_result)
        db.session.commit()

        # 如果需要，发送邮件预警
        handle_alert(alert_level, sensitive_words, weibo_comment, current_app)

    return redirect(url_for('routes.index'))

@bp.route('/stats')
def stats():
    """
    返回统计数据，包括危险等级分布、敏感词总数、按时间的评论数量等。
    """
    # 危险等级列表
    levels = ['常态', '较大', '重大', '特别重大']

    # 按时间和危险等级统计评论数量

    time_data = {}
    for level in levels:
        query = (
            db.session.query(
                func.date(WeiboComment.created_at).label("date"),
                func.count(WeiboComment.id).label("count")
            )
            .join(AnalysisResult, AnalysisResult.comment_id == WeiboComment.id)
            .filter(AnalysisResult.alert_level == level)
            .group_by(func.date(WeiboComment.created_at))
            .order_by("date")
            .all()
        )
        time_data[level] = {
            "dates": [str(row.date) for row in query] if query else [],
            "counts": [row.count for row in query] if query else [],
        }

    # 其他统计数据
    stats_data = {
        "level_counts": {level: AnalysisResult.query.filter_by(alert_level=level).count() for level in levels},
        "time_series": time_data,
        "total_comments": WeiboComment.query.count(),
        "total_sensitive_words": db.session.query(
            db.func.sum(db.func.json_length(AnalysisResult.sensitive_words))
        ).scalar() or 0,
    }

    return render_template('stats.html', stats=stats_data)

# 从数据库中接取然后分析

# 用于控制自动化分析的运行状态
stop_event = Event()

@bp.route('/automate', methods=['POST'])
def automate_analysis():
    """
    持续分析未处理的评论，直到手动停止。
    """
    # 提取触发动作（开始或停止）
    action = request.json.get('action', 'start')

    if action == 'stop':
        # 停止分析任务
        stop_event.set()
        return jsonify({"message": "分析已停止"})

    # 重置停止标志
    stop_event.clear()

    while not stop_event.is_set():
        # 查找一条未分析的评论
        comment = WeiboComment.query.filter_by(analyzed=False).first()

        if not comment:
            # 如果没有未分析的评论，等待新的数据
            print("没有未分析的评论，等待中...")
            sleep(5)  # 等待 5 秒再检查
            continue

        # 调用分析逻辑
        # 调用敏感性分析逻辑
        sensitive_words = evaluate_weibo_content(comment.text)

        # 根据分析结果确定危险等级
        if sensitive_words:
            alert_level = max(word['level'] for word in sensitive_words)
        else:
            alert_level = "常态"

        # 保存分析结果到分析表
        analysis_result = AnalysisResult(
            comment_id=comment.id,
            sensitive_words=json.dumps(sensitive_words),
            alert_level=alert_level,
            created_at=comment.created_at
        )

        db.session.add(analysis_result)

        # 标记评论为已分析
        comment.analyzed = True

        # 提交数据库更改
        db.session.commit()

        # 如果分析结果达到某个等级，则发送邮件提醒
        handle_alert(alert_level, sensitive_words, comment, current_app)

        print(f"评论 {comment.id} 已分析: {alert_level}")

    return jsonify({"message": "分析任务已启动"})
