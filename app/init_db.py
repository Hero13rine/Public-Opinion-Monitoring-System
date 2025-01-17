from app import create_app, db
from flask import current_app

# 定义数据库模型
class WeiboComment(db.Model):
    __tablename__ = 'weibo_comments'
    id = db.Column(db.Integer, primary_key=True)
    weibo_id = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('weibo_comments.id'), nullable=False)
    sensitive_words = db.Column(db.JSON, nullable=False)
    alert_level = db.Column(db.String(32), nullable=False)

def initialize_database():
    """
    初始化数据库：创建所有表并插入初始数据
    """
    app = create_app()
    with app.app_context():
        # 确保在应用上下文中创建表
        db.create_all()
        print("数据库表已创建！")

        # 插入初始测试数据
        insert_mock_data()

def insert_mock_data():
    """
    向数据库插入测试数据
    """
    # 测试数据
    mock_comments = [
        {"weibo_id": "mock1", "text": "这是普通的测试内容，无敏感词。"},
        {"weibo_id": "mock2", "text": "这条内容包含重大敏感词，应该触发警报。"},
        {"weibo_id": "mock3", "text": "特别重大事件，测试特别重大警报。"},
    ]

    for comment in mock_comments:
        new_comment = WeiboComment(weibo_id=comment["weibo_id"], text=comment["text"])
        db.session.add(new_comment)
    db.session.commit()
    print("测试数据已插入！")

if __name__ == "__main__":
    initialize_database()
