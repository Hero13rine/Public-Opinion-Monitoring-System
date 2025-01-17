from app.services.spider import Spider
from app.services.evaluation import evaluate_comment
from app.services.email import send_email
from app.models import db, WeiboComment, AnalysisResult

def run_tasks():
    # Step 1: 爬取评论
    spider = Spider()
    comments = spider.fetch_comments()

    for comment in comments:
        # Step 2: 存储评论
        weibo_comment = WeiboComment(weibo_id=comment['weibo_id'], text=comment['text'])
        db.session.add(weibo_comment)
        db.session.commit()

        # Step 3: 分析评论
        analysis = evaluate_comment(comment['text'])
        alert_level = analysis['alert_level']

        # Step 4: 存储分析结果
        analysis_result = AnalysisResult(
            comment_id=weibo_comment.id,
            sensitive_words=analysis['sensitive_words'],
            alert_level=alert_level
        )
        db.session.add(analysis_result)
        db.session.commit()

        # Step 5: 发送邮件（根据等级）
        if alert_level in ['重大', '特别重大']:
            send_email(
                subject=f"预警：发现{alert_level}内容",
                body=f"评论内容：{comment['text']}\n等级：{alert_level}\n敏感词：{', '.join(analysis['sensitive_words'])}",
                to='admin@example.com'
            )
