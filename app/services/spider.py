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
#todo 现在生成自动化生成测试脚本，可以写一个调用大模型生成的，生成的内容要符合json格式要求，然后添加到评论数据库中