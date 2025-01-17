from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import WeiboComment  # 假设模型定义在 models.py

# 配置数据库连接
DATABASE_URI = "mysql+pymysql://root:root@localhost:3308/weibo_analysis"
engine = create_engine(DATABASE_URI)

# 创建只读会话
Session = sessionmaker(bind=engine)
session = Session()

def fetch_first_analyzed_comment():
    """
    查询数据库中第一条已分析的评论
    """
    try:
        # 查询第一条 analyzed=True 的评论
        comment = session.query(WeiboComment).filter_by(analyzed=True)
        for comment in comment:
            if comment:
                print(comment.text)
            else:
                print("未找到已分析的评论")
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        # 关闭会话
        session.close()

if __name__ == "__main__":
    fetch_first_analyzed_comment()
