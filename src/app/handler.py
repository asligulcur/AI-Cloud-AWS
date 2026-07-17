import json

from qa_service import answer_question


def lambda_handler(event, context):
    """API Gateway (HTTP API) proxy handler for POST /ask."""
    try:
        body = json.loads(event.get("body") or "{}")
        question = body.get("question", "")
        result = answer_question(question)
        status = 200
    except ValueError as exc:
        result = {"error": str(exc)}
        status = 400

    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }
