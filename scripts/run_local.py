#!/usr/bin/env python3
"""Run the Q&A logic locally without deploying anything to AWS.

Usage:
    python scripts/run_local.py "What is an S3 bucket?"

If no AWS credentials or Bedrock model access are available, this will
gracefully print a stubbed response instead of failing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "app"))

from qa_service import answer_question  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print('usage: run_local.py "your question"')
        raise SystemExit(1)

    question = " ".join(sys.argv[1:])
    result = answer_question(question)
    print(f"[{result['source']}] {result['answer']}")


if __name__ == "__main__":
    main()
