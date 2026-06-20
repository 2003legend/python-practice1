"""
Day9: RAG 核心逻辑（检索 + 生成）

RAG 流程：
1. 把文档切成小块 chunk
2. 存入向量库（语义检索）
3. 用户提问 → 检索最相关的 chunk
4. 把 chunk 拼进 prompt → 大模型回答

首次使用先构建索引：
    python day09_rag_build.py

然后测试问答：
    python day09_rag_query.py
"""

import os
import re

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "learning_notes"


def get_llm_client() -> OpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("请先在 .env 里配置 DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def get_collection(recreate: bool = False):
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    if recreate:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return client.get_or_create_collection(name=COLLECTION_NAME)


def load_markdown_files() -> list[tuple[str, str]]:
    files = []
    if not os.path.isdir(DOCS_DIR):
        return files
    for name in os.listdir(DOCS_DIR):
        if name.endswith(".md"):
            path = os.path.join(DOCS_DIR, name)
            with open(path, encoding="utf-8") as f:
                files.append((name, f.read()))
    return files


def split_into_chunks(text: str, chunk_size: int = 120) -> list[str]:
    """按段落切分，太长的段落再按长度切。"""
    paragraphs = [p.strip() for p in re.split(r"\n+", text) if p.strip()]
    chunks = []
    for para in paragraphs:
        if para.startswith("#"):
            continue
        while len(para) > chunk_size:
            chunks.append(para[:chunk_size])
            para = para[chunk_size:]
        if para:
            chunks.append(para)
    return chunks


def build_index() -> int:
    files = load_markdown_files()
    if not files:
        raise RuntimeError(f"docs 目录为空，请先添加 .md 文件：{DOCS_DIR}")

    collection = get_collection(recreate=True)

    ids, documents, metadatas = [], [], []
    idx = 0
    for filename, content in files:
        for chunk in split_into_chunks(content):
            ids.append(f"chunk-{idx}")
            documents.append(chunk)
            metadatas.append({"source": filename})
            idx += 1

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return len(documents)


def retrieve(question: str, top_k: int = 3) -> list[str]:
    collection = get_collection()
    if collection.count() == 0:
        raise RuntimeError("索引为空，请先运行 python day09_rag_build.py")
    result = collection.query(query_texts=[question], n_results=top_k)
    return result["documents"][0]


def ask_with_rag(question: str, top_k: int = 3) -> dict:
    chunks = retrieve(question, top_k=top_k)
    context = "\n".join(f"- {c}" for c in chunks)

    prompt = f"""请根据以下资料回答问题。
如果资料里没有相关信息，请明确说「资料中没有提到」。

【资料】
{context}

【问题】
{question}
"""

    client = get_llm_client()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是严谨的学习助手，只根据给定资料回答。"},
            {"role": "user", "content": prompt},
        ],
    )
    answer = response.choices[0].message.content
    return {"question": question, "context": chunks, "answer": answer}
