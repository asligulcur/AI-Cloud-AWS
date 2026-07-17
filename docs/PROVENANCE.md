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
| 2026-07-17 | Entire initial scaffold: `.devcontainer/`, `src/app/`, `infra/template.yaml`, `frontend/index.html`, `scripts/`, `tests/`, `docs/ARCHITECTURE.md`, this file, `README.md`, `.gitignore`, `.github/workflows/ci.yml` | Agent-generated (Claude Code) | "Build a working, defensible starting architecture for an AI Cloud course assignment in the AWS Academy Learner Lab sandbox: devcontainer, repo structure, a question-in/model-response-out prototype (stub acceptable), architecture diagram, narrative, and this provenance log." | _Pending — fill in your name(s) here_ | **Pending team review.** Locally verified before commit: `python scripts/run_local.py "..."` runs end-to-end and returns a stubbed answer (no AWS credentials present in the dev environment); `pytest` passes (4/4 tests) covering input validation and the stub fallback path. Not yet verified: an actual `sam deploy` into a live Learner Lab account, or a real (non-stub) Bedrock response. |

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
