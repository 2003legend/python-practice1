"""
Day8-2: FastAPI + 大模型聊天接口

1. 确保 .env 里已配置 DEEPSEEK_API_KEY
2. 启动：uvicorn day08_fastapi_llm:app --reload --port 8000
3. 打开 http://127.0.0.1:8000/docs
4. 测试 POST /chat，body 示例：{"message": "Python 里 list 和 tuple 有什么区别？"}
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="LLM 聊天 API")

api_key = os.getenv("DEEPSEEK_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def read_root():
    return {
        "message": "LLM 聊天 API",
        "docs": "/docs",
        "api_ready": client is not None,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="未配置 DEEPSEEK_API_KEY，请创建 .env 文件",
        )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个简洁友好的编程助教，回答尽量简短。"},
            {"role": "user", "content": req.message},
        ],
    )
    reply = response.choices[0].message.content
    return ChatResponse(reply=reply)
