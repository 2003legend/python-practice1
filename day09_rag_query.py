"""命令行测试 RAG：python day09_rag_query.py"""

from day09_rag_core import ask_with_rag

if __name__ == "__main__":
    questions = [
        "Git 和 GitHub 有什么区别？",
        "HAVING 和 WHERE 有什么区别？",
        "我竞赛拿过什么奖？",
    ]
    for q in questions:
        print("=" * 50)
        print("问:", q)
        result = ask_with_rag(q)
        print("检索到:", result["context"])
        print("答:", result["answer"])
        print()
