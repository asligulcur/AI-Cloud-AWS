# AI Cloud — Q&A Starter

A minimal, serverless Q&A prototype and starting cloud architecture, built
for deployment in the **AWS Academy Learner Lab** sandbox. Accepts a
question, calls Amazon Bedrock for a model-generated answer, and falls back
to a clearly-labeled stub if Bedrock isn't reachable yet — so the prototype
runs today even before model access is configured.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design
narrative and diagram, and [`docs/PROVENANCE.md`](docs/PROVENANCE.md) for
what in this repo is human-written vs. agent-generated.

## Repo structure

```
.
├── .devcontainer/       # Dev Containers config (Python + AWS CLI, ready to code)
├── src/app/             # Lambda handler + core Q&A service logic
├── infra/template.yaml  # AWS SAM template (API Gateway + Lambda + DynamoDB)
├── frontend/            # Minimal static HTML/JS client
├── scripts/             # run_local.py (no-AWS local run), deploy.sh (SAM deploy)
├── tests/               # pytest suite for the Q&A service
├── docs/                # Architecture narrative, diagram, provenance log
└── .github/workflows/   # CI: runs the test suite on push/PR
```

## Conventions

- **Core logic lives in `src/app/qa_service.py`**, decoupled from the Lambda
  entry point (`handler.py`) so it can run and be tested without any AWS
  dependency. If you add features, keep that split — logic in
  `qa_service.py`, AWS glue in `handler.py`.
- **Fail toward the stub, never toward an error.** Anything that calls
  Bedrock (or, later, other external services) should catch failures and
  return the stub response rather than raising — a Lab environment with
  flaky model access shouldn't mean a broken demo.
- **No custom IAM roles.** The Learner Lab sandbox only provides `LabRole`.
  Any new resource needing permissions should reference `LabRoleArn`
  (see `infra/template.yaml`), not a newly-defined role/policy.
- **No idle-cost resources.** Stick to pay-per-request services (Lambda,
  API Gateway HTTP API, DynamoDB on-demand, Bedrock). Avoid EC2, NAT
  gateways, load balancers, or anything else that bills while sitting idle
  between Lab sessions, per the Lab's own budget warning.
- **Update `docs/PROVENANCE.md`** in the same change that adds or edits
  code — mark what's agent-generated, note what you (the reviewer) actually
  ran and checked.

## Prerequisites

- [Docker](https://www.docker.com/) + [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  (or GitHub Codespaces) — recommended, gives you Python + AWS CLI + SAM CLI
  out of the box.
- Alternatively, locally: Python 3.12+, and `pip install -r requirements-dev.txt`.
- An active AWS Academy Learner Lab session, if you want to deploy (not
  required to run the prototype locally).

## Clone and run

```bash
git clone <this-repo-url>
cd ai-cloud-qa-starter
pip install -r requirements-dev.txt   # or: reopen in the dev container
```

**Run the prototype locally (no AWS needed):**

```bash
python scripts/run_local.py "What is an S3 bucket?"
# [stub] This is a stubbed response. ...
```

**Run the tests:**

```bash
pytest
```

**Try the frontend:** open `frontend/index.html` directly in a browser. It
will fail to reach an API until one is deployed (see below) — that's
expected.

## Deploying to the AWS Academy Learner Lab

1. Start your Lab session and copy the temporary credentials from
   **AWS Details > AWS CLI** into `~/.aws/credentials`.
2. Get your Lab's execution role ARN:
   ```bash
   export LAB_ROLE_ARN=$(aws iam get-role --role-name LabRole --query Role.Arn --output text)
   ```
3. (Optional, for live answers instead of the stub) In the Bedrock console,
   under **Model access**, enable the model referenced by
   `BEDROCK_MODEL_ID` in `infra/template.yaml` (default: Claude Haiku).
4. Deploy:
   ```bash
   ./scripts/deploy.sh
   ```
5. Point the frontend at the deployed API: open `frontend/index.html` with
   `window.API_URL` set to the `ApiUrl` output from the deploy, e.g. via the
   browser console, or by editing the `API_URL` constant directly.

**Budget note:** everything here is pay-per-request. Nothing bills while
idle, but it's still good practice to `sam delete --stack-name
ai-cloud-qa-starter` when you're done for the term.

## License

Course project — no license specified yet.
