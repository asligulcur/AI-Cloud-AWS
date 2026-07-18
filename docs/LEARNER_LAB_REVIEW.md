# Learner Lab Review — Findings & Next Steps

Review of the AWS Academy Learner Lab environment docs (instructions dated
2025-06-24) against the architecture in this repo, plus the resulting
checklist.

## What matches our design (confirmed good)

- API Gateway, Lambda, DynamoDB, CloudWatch, Secrets Manager, SSM, and S3
  are all explicitly supported and can assume `LabRole` — exactly what
  `infra/template.yaml` relies on.
- IAM section confirms: *"You cannot create roles, except service-linked
  roles"* — validates attaching `LabRole` directly rather than defining a
  custom role/policy.
- The budget guidance singles out EC2, RDS, NAT Gateway, EMR, SageMaker,
  and Elastic Beanstalk as the real cost risks — confirms avoiding all of
  those in favor of a serverless design was the right call.

## What's a problem: Amazon Bedrock is not on the supported-services list

The Lab's service list is thorough (it even includes DeepRacer and
DeepComposer), and Bedrock doesn't appear anywhere in it. That's the core
"model-generated response" component of our design. It may still be
reachable in this specific account (the list isn't guaranteed exhaustive
across every course variant), but it needs verifying before assuming live
answers will work — the stub fallback means the prototype still runs
either way, but the architecture narrative should reflect what's actually
true in this account, not just the intended design.

## Other details worth noting

- Region is locked to `us-east-1` / `us-west-2` — the deploy script
  doesn't currently pin a region, should fix.
- Lambda caps at 10 concurrent execution environments — irrelevant for a
  demo, just noting.

## Resolution (2026-07-18)

Deployed for real via AWS CloudShell against account `485762611572` in
`us-east-1`. Two issues turned up and were fixed along the way:

1. **Region**: `scripts/deploy.sh` didn't pin a region — fixed, now
   defaults to `us-east-1` (overridable via `AWS_REGION`).
2. **Python runtime mismatch**: `sam build` failed locally because
   CloudShell only has Python 3.13 installed, not the 3.12 the template
   asked for, and CloudShell has no Docker for a `--use-container` build.
   Fixed by bumping `infra/template.yaml`'s Lambda runtime to
   `python3.13` (a supported Lambda runtime) to match what's actually on
   CloudShell's PATH.

After those fixes, the stack (`ai-cloud-qa-starter`) deployed cleanly and
`curl`-ing the live `/ask` endpoint returned a valid JSON response.
**Confirmed: Bedrock is not currently reachable from this account** — the
deployed Lambda's `InvokeModel` call fails over to the stub path, matching
the earlier suspicion that Bedrock is absent from this Lab's
supported-services list. Decision for now: **ship stub-only**; live model
access (Bedrock or a direct Anthropic API call) is a follow-up, not a
blocker for this submission.

A third issue turned up testing the actual frontend (not just `curl`) in a
browser: the API Gateway HTTP API had no CORS configuration, so
`fetch()` from `frontend/index.html` failed even though `curl` worked fine
(curl doesn't enforce CORS; browsers do). Fixed by adding
`HttpApi.CorsConfiguration` (`AllowOrigins: ["*"]`) to
`infra/template.yaml` and redeploying. Separately, opening the frontend
via a bare `file://` URL failed in Safari specifically (it restricts
`fetch()` from that origin); serving it locally via
`python3 -m http.server` resolved that. With both fixes in place, the
frontend was confirmed working end-to-end in an actual browser, not just
via `curl`.

## Checklist — next steps

- [x] Start a Lab session and check whether Bedrock is reachable —
      confirmed not reachable via a live deployed `InvokeModel` call.
- [ ] ~~If Bedrock works: enable Claude Haiku access~~ — deferred; not
      pursuing for this submission.
- [x] Decided: staying stub-only for now, per the assignment's own
      allowance for a stubbed response.
- [x] Pinned the deploy region to `us-east-1` in `scripts/deploy.sh`.
- [x] Got temporary credentials via AWS CloudShell (no manual credential
      copying needed).
- [x] Got the LabRole ARN: `arn:aws:iam::485762611572:role/LabRole`.
- [x] Ran `./scripts/deploy.sh` — stack `ai-cloud-qa-starter` created
      successfully.
- [x] Hit the deployed `/ask` endpoint — confirmed valid JSON response
      (stub).
- [x] Updated `docs/ARCHITECTURE.md` to reflect the real, verified state.
- [x] Updated `docs/PROVENANCE.md` with actual review/deployment notes.
- [ ] Watch the budget banner; `sam delete --stack-name
      ai-cloud-qa-starter --region us-east-1` when done for the day/term.
