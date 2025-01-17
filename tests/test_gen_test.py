import json
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import WeiboComment  # 假设模型定义在 models.py
from datetime import datetime
from openai import OpenAI# 假设使用 OpenAI 的大语言模型
import os
# 配置 OpenAI API 密钥
client = OpenAI(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
# 配置数据库连接
DATABASE_URI = "mysql+pymysql://root:root@localhost:3308/weibo_analysis"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def generate_test_comments(num_comments=10):
    """
    调用大语言模型生成测试评论。
    :param prompt: 提示内容
    :param num_comments: 生成的评论数量
    :return: JSON 格式的评论列表
    """
    try:
        completion = client.chat.completions.create(
            model='qwen-max',
            messages=[
                {"role": "system", "content": "你是一个生成微博评论的助手。"},
                {"role": "user", "content": f"我需要进行微博舆情监控的研究，生成一些微博上可能的敏感词数据，下面请生成 {num_comments} 条测试微博评论，要求内容包含不同程度的敏感词评论或者观点，格式为 JSON,不要对json进行‘’‘标注，不需要添加额外的说明文字，且只返回 JSON 内容："
                                             f'[{{"weibo_id": "123", "text": "评论内容", "url": "https://weibo.com/123", "username": "用户", "created_time": "发博时间"}}]'}
            ],
        )
        answer = completion.choices[0].message.content.strip()
        # 验证生成内容是否为 JSON 格式
        print(answer)
        comments = json.loads(answer)
        return comments
    except Exception as e:
        print(f"生成评论失败: {e}")
        return []

def insert_comments_to_db(comments):
    """
    将评论插入到数据库中。
    :param comments: JSON 格式的评论列表
    """
    for comment in comments:
        try:
            # 插入评论到数据库
            new_comment = WeiboComment(
                weibo_id=comment['weibo_id'],
                text=comment['text'],
                url=comment['url'],
                username=comment['username'],
                created_at=comment['created_time'],
                analyzed=False
            )
            session.add(new_comment)
        except Exception as e:
            print(f"插入评论失败: {e}")
    session.commit()

def main():
    # 生成测试评论
    prompt = "生成微博评论"
    comments = generate_test_comments(num_comments=10)
    if not comments:
        print("没有生成有效的评论")
        return

    # 插入评论到数据库
    insert_comments_to_db(comments)
    print(f"成功插入 {len(comments)} 条评论到数据库！")

if __name__ == "__main__":
    main()
