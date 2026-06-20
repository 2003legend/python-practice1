"""构建 RAG 索引：python day09_rag_build.py"""

from day09_rag_core import build_index

if __name__ == "__main__":
    count = build_index()
    print(f"索引构建完成，共 {count} 个文本块")
