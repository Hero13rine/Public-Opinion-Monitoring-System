class Spider:
    def fetch_comments(self):
        """
        爬取微博内容，并返回包含 URL、用户名和文本的评论列表。
        示例返回数据：
        [
            {"url": "https://weibo.com/123456", "username": "用户A", "text": "测试评论内容1"},
            {"url": "https://weibo.com/789012", "username": "用户B", "text": "测试评论内容2"}
        ]
        """
        # 模拟爬取数据
        return [
            {"url": "https://weibo.com/123456", "username": "用户A", "text": "测试评论内容1"},
            {"url": "https://weibo.com/789012", "username": "用户B", "text": "测试评论内容2"}
        ]
