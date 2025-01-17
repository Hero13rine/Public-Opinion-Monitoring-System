import json
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)

def evaluate_weibo_content(weibo_text):
    prompt = f"""
        请分析以下微博内容中的敏感词，并按照危险程度进行分类。危险程度分为四级：特别重大、重大、较大和常态。
        其中常态是可能出现校内讨论，较大是可能出现焦虑心理，重大是可能导致抑郁和部分政治讨论，特别重大为可能出现极大政治风险或者生命安全风险
        请严格按照以下 JSON 格式返回结果：

        {{
            "sensitive_words": [
                {{
                    "word": "敏感词1",
                    "level": "特别重大"
                }},
                {{
                    "word": "敏感词2",
                    "level": "重大"
                }}
                // 继续添加敏感词对象
            ]
        }}

        注意：
        - 如果没有敏感词，请将 "sensitive_words" 设置为空数组 []。
        - 返回的 JSON 必须是有效的，不包含注释或多余的符号。
        - 不需要添加额外的说明文字，只返回 JSON 内容。

        微博内容:
        "{weibo_text}"
        """
    try:
        completion = client.chat.completions.create(
            model='qwen-max',
            messages=[
                {'role': 'system', 'content': '你是一个内容审核助手。'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0
        )
        answer = completion.choices[0].message.content.strip()
        return json.loads(answer).get('sensitive_words', [])
    except Exception as e:
        return []
