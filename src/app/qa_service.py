import json
import os
import time
import uuid

import boto3

BEDROCK_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
)
STUB_MODE = os.environ.get("STUB_MODE", "").lower() in ("1", "true", "yes")

_STUB_ANSWER = (
    "This is a stubbed response. Live model access has not been configured for "
    "this environment yet (either STUB_MODE is set, or the Bedrock call failed) "
    "— enable the model in the AWS Academy Learner Lab Bedrock console and "
    "retry to get a real answer."
)


def answer_question(question: str) -> dict:
    """Answer a question via Bedrock, falling back to a stub on any failure."""
    if not question or not question.strip():
        raise ValueError("question must be a non-empty string")

    if STUB_MODE:
        result = {"answer": _STUB_ANSWER, "source": "stub"}
    else:
        result = _invoke_bedrock(question)

    _log_interaction(question, result)
    return result


def _invoke_bedrock(question: str) -> dict:
    try:
        client = boto3.client("bedrock-runtime")
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [{"role": "user", "content": question}],
            }
        )
        response = client.invoke_model(modelId=BEDROCK_MODEL_ID, body=body)
        payload = json.loads(response["body"].read())
        answer = payload["content"][0]["text"]
        return {"answer": answer, "source": "bedrock"}
    except Exception:
        return {"answer": _STUB_ANSWER, "source": "stub"}


def _log_interaction(question: str, result: dict) -> None:
    """Best-effort write to the Q&A log table. Never raises."""
    table_name = os.environ.get("QA_LOG_TABLE")
    if not table_name:
        return
    try:
        table = boto3.resource("dynamodb").Table(table_name)
        table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "question": question,
                "answer": result["answer"],
                "source": result["source"],
                "timestamp": int(time.time()),
            }
        )
    except Exception:
        pass
