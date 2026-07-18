# Code Provenance Log

This log tracks what was human-written vs. agent-generated, and what review
each piece has had. Update it in the same PR/commit that introduces or
changes the code it describes — a provenance entry that lags the code it
describes isn't trustworthy.

## Roles (per the course's AI Use Modes)

- **Operator** — the human directing the agent: sets the task, constraints,
  and acceptance criteria, and decides what to keep.
- **Agent** — the AI (here, Claude Code) generating code/config from the
  Operator's direction.
- **Critic** — the human (can be the same person as Operator, or a
  teammate) who reads, runs, and tests the agent's output before it's
  trusted. "Code you can't explain is code you don't control" — the Critic
  step is what closes that gap.

## Log

| Date | Component / file(s) | Origin | Operator prompt (summary) | Reviewed by | Review status / notes |
|---|---|---|---|---|---|
| 2026-07-17 | Entire initial scaffold: `.devcontainer/`, `src/app/`, `infra/template.yaml`, `frontend/index.html`, `scripts/`, `tests/`, `docs/ARCHITECTURE.md`, this file, `README.md`, `.gitignore`, `.github/workflows/ci.yml` | Agent-generated (Claude Code) | "Build a working, defensible starting architecture for an AI Cloud course assignment in the AWS Academy Learner Lab sandbox: devcontainer, repo structure, a question-in/model-response-out prototype (stub acceptable), architecture diagram, narrative, and this provenance log." | asligulcur | **Reviewed.** Locally verified before commit: `python scripts/run_local.py "..."` runs end-to-end and returns a stubbed answer; `pytest` passes (4/4 tests). Superseded by the 2026-07-18 deployment entry below, which verified the full stack live in AWS. |
| 2026-07-18 | `infra/template.yaml` (runtime bump python3.12 → python3.13), `scripts/deploy.sh` (region pin), `frontend/index.html` (default `API_URL`), `docs/ARCHITECTURE.md`, `docs/DEPLOYMENT.md`, `docs/LEARNER_LAB_REVIEW.md` | Agent-generated (Claude Code), fixes driven by live errors the Operator hit and pasted back | Operator ran the actual deployment in AWS CloudShell step-by-step (Critic role in real time): hit and reported a Python-version build failure, which the Agent diagnosed (CloudShell ships Python 3.13, no matching 3.12 binary, no Docker for `--use-container`) and fixed by bumping the template's Lambda runtime. | asligulcur | **Reviewed — deployed and hands-on verified.** Operator personally ran every step in AWS CloudShell (clone, `sam build`, `sam deploy`) against the real Learner Lab account (485762611572, us-east-1) and confirmed via `curl` that the deployed `/ask` endpoint returns a valid JSON response. Confirmed finding: Bedrock is not currently reachable from this account (`InvokeModel` fails over to the stub path), consistent with Bedrock's absence from the Lab's supported-services list. Deployed stack: `ai-cloud-qa-starter`. |
| 2026-07-18 | `infra/template.yaml` (added `HttpApi.CorsConfiguration`) | Agent-generated (Claude Code), fix driven by a live browser error the Operator hit | Operator tried the actual frontend (`frontend/index.html`) in a browser against the live deployment and got a fetch failure. Agent diagnosed the API Gateway HTTP API had no CORS headers configured (curl doesn't enforce CORS, so the earlier curl-only verification hadn't caught it), added `AllowOrigins: ["*"]` for `POST`/`Content-Type`, redeployed. | asligulcur | **Reviewed — hands-on verified in-browser.** Operator redeployed after the fix and confirmed the frontend (served over `python3 -m http.server`, not opened via bare `file://` — Safari blocks fetch from that origin) successfully renders a stub answer end-to-end. This is the first entry verified via the actual UI rather than just `curl`. |
| 2026-07-18 | `README.md` (clone URL/dir name, "try the frontend" instructions, Bedrock framing, live-endpoint POST-only clarification, full rewrite of the Learner Lab deploy steps) | Agent-generated (Claude Code) | Operator asked for a fresh read-through of the repo "as a stranger would read it," then separately flagged that the live API URL looked clickable but returned a blank screen, and asked whether the README made that clear. Agent found and fixed each stale/ambiguous spot as reported. | asligulcur | **Reviewed.** Each fix was made in direct response to something the Operator personally hit (stale clone command was never actually run against test; the blank-screen confusion was a real, reported UX issue) rather than speculative cleanup. `pytest` re-run (4/4 passing) after each edit. |

## What "reviewed" should mean going forward

Before checking a row's status from "Pending" to a reviewer's name, the
Critic should have actually:

- Read the diff, not just the summary.
- Run it (`pytest`, and/or `scripts/run_local.py` for anything touching
  `qa_service.py`).
- For anything touching `infra/template.yaml`: run `sam deploy` in the Lab
  and confirm the stack comes up and `/ask` responds.
- Understood *why* the code is shaped the way it is well enough to explain
  it without the agent's help — if it's not explainable, it's not reviewed.

Add a new row per meaningfully-sized change (a feature, a fix, an infra
change) rather than editing history — this file is a log, not a snapshot.
