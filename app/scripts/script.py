from app.models import db, WeiboComment, AnalysisResult
from app.services.evaluation import evaluate_weibo_content
from app.services.email import send_alert_email

def analyze_and_alert():
    comments = WeiboComment.query.all()
    for comment in comments:
        sensitive_words = evaluate_weibo_content(comment.text)
        if sensitive_words:
            result = AnalysisResult(comment_id=comment.id, sensitive_words=sensitive_words, alert_level=max(word['level'] for word in sensitive_words))
            db.session.add(result)
            if result.alert_level in ['重大', '特别重大']:
                send_alert_email(sensitive_words, comment.text)
    db.session.commit()
