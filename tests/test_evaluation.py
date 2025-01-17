import os
import json
from openai import OpenAI

# 配置 OpenAI 客户端
api_key = os.getenv("DASHSCOPE_API_KEY")  # 或直接替换为你的 API Key
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # Dashscope 的基础 URL

if not api_key:
    print("请确保已设置环境变量 DASHSCOPE_API_KEY 或直接替换 API Key。")
    exit(1)

client = OpenAI(api_key=api_key, base_url=base_url)


def test_functionality(test_cases):
    """
    测试模型功能，通过多个测试案例验证输出是否符合预期。

    参数:
        test_cases (list): 测试案例列表，每个案例包含 `input` 和 `description`。
    """
    for idx, case in enumerate(test_cases, 1):
        print(f"测试案例 {idx}: {case['description']}")
        prompt = f"""
        请分析以下微博内容中的敏感词，并按照危险程度进行分类。危险程度分为四级：特别重大、重大、较大和常态。
        微博内容: "{case['input']}"
        返回格式: JSON 包含敏感词和危险等级。
        """
        try:
            # 调用模型 API
            response = client.chat.completions.create(
                model="qwen-max",  # 根据实际需要选择模型
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            # 解析响应
            result = response.choices[0].message.content.strip()
            print(f"模型响应:\n{result}\n")
        except Exception as e:
            print(f"测试案例 {idx} 失败，错误信息: {e}\n")


if __name__ == "__main__":
    # 定义测试案例
    test_cases = [
        {
            "input": "今天的天气真好，适合出去散步！",
            "description": "普通文本，不应检测到敏感词。",
        },
        {
            "input": "这是一个包含敏感词1的测试句子。",
            "description": "包含敏感词1，应返回敏感词信息。",
        },
        {
            "input": "",
            "description": "空输入，应返回错误提示。",
        },
        {
            "input": "涉及政治敏感内容的文本。",
            "description": "包含重大敏感词，应正确分类为‘重大’或‘特别重大’。",
        }
    ]

    # 运行测试
    test_functionality(test_cases)
