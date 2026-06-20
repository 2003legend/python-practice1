"""
Day9: FastAPI + RAG 知识库问答

1. 确保 .env 已配置 DEEPSEEK_API_KEY
2. 构建索引：python day09_rag_build.py
3. 启动：uvicorn day09_fastapi_rag:app --reload
4. 打开 http://127.0.0.1:8000/docs ，测试 POST /ask
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from day09_rag_core import ask_with_rag

app = FastAPI(title="RAG 知识库问答")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    context: list[str]
    answer: str


@app.get("/")
def read_root():
    return {"message": "RAG 知识库问答", "docs": "/docs"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        result = ask_with_rag(req.question)
        return AskResponse(**result)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
