"""
Day8-1: 第一次调用大模型 API

1. pip install openai python-dotenv
2. 复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY
3. 运行本文件：python day08_llm_test.py
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")


def ask_llm(question: str) -> str:
    if not api_key:
        raise RuntimeError("请先在 .env 里配置 DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个简洁的编程助教。"},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(ask_llm("用三句话解释什么是大模型 API。"))
