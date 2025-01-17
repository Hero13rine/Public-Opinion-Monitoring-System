from . import db

class WeiboComment(db.Model):
    __tablename__ = 'weibo_comments'
    id = db.Column(db.Integer, primary_key=True)
    weibo_id = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=False)  # 新增：微博的定位网址
    username = db.Column(db.String(64), nullable=False)  # 新增：用户名
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    analyzed = db.Column(db.Boolean, default=False)  # 是否已检测，默认未检测
class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('weibo_comments.id'), nullable=False)
    sensitive_words = db.Column(db.JSON, nullable=False)
    alert_level = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # 定义关系
    comment = db.relationship('WeiboComment', backref='analysis_results')
