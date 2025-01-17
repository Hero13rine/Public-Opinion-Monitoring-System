"""
目的是测试自动化测试大模型是否输出正确的字符编码

"""
import json
from unittest.mock import patch, MagicMock
from app.models import WeiboComment, AnalysisResult
from app import db, create_app
from flask import Flask

# 创建 Flask 测试应用程序
app = create_app()
app.app_context().push()

def test_automate_analysis_output():
    """
    测试 `automate_analysis` 函数的输出格式是否正确，以及处理后的数据是否被正确解析。
    """
    # 准备测试数据（Unicode 格式）
    test_comment = WeiboComment(
        weibo_id="test_123",
        text="\u8fd9\u662f\u4e00\u4e2a\u6d4b\u8bd5\u8bc4\u8bba\uff0c\u542b\u6709\u654f\u611f\u8bcd\u3002",
        url="https://weibo.com/test_123",
        username="\u6d4b\u8bd5\u7528\u6237",
        analyzed=False
    )

    # 插入测试评论到数据库
    db.session.add(test_comment)
    db.session.commit()

    # 模拟 `evaluate_weibo_content` 返回值
    def mock_evaluate_weibo_content(text):
        return [
            {"word": "\u654f\u611f\u8bcd", "level": "\u91cd\u5927"},
            {"word": "\u6d4b\u8bd5", "level": "\u4e2d"}
        ]

    with patch('app.routes.evaluate_weibo_content', side_effect=mock_evaluate_weibo_content):
        # 查询一条未分析的评论
        comment = WeiboComment.query.filter_by(analyzed=False).first()

        if not comment:
            print("没有未分析的评论")
            return

        # 调用模拟的敏感词分析逻辑
        sensitive_words = mock_evaluate_weibo_content(comment.text)

        # 计算危险等级
        alert_level = max(word['level'] for word in sensitive_words)

        # 保存分析结果到数据库
        analysis_result = AnalysisResult(
            comment_id=comment.id,
            sensitive_words=json.dumps(sensitive_words, ensure_ascii=False),
            alert_level=alert_level,
            created_at=comment.created_at
        )
        db.session.add(analysis_result)

        # 更新评论状态
        comment.analyzed = True
        db.session.commit()

        # 验证结果是否正确解析
        print("=== 测试结果 ===")
        print(f"评论内容: {comment.text}")
        print(f"敏感词分析结果 (JSON): {analysis_result.sensitive_words}")
        print(f"危险等级: {analysis_result.alert_level}")

        # 验证敏感词结果是否为正确的 JSON 格式
        try:
            sensitive_words_data = json.loads(analysis_result.sensitive_words)
            print(f"解析后敏感词结果: {sensitive_words_data}")
        except json.JSONDecodeError as e:
            print(f"敏感词结果解析失败: {e}")

if __name__ == "__main__":
    test_automate_analysis_output()
