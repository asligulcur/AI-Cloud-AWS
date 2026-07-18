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

## Checklist — next steps

- [ ] **Start a Lab session and check the Bedrock console directly**
      (search "Bedrock" in us-east-1) — does it load, and is there a
      Model access page? This one finding determines everything below.
- [ ] **If Bedrock works:** request/enable access to the Claude Haiku
      model, deploy, and confirm live (non-stub) answers.
- [ ] **If Bedrock is blocked/absent:** decide between (a) staying
      stub-only for submission — fully acceptable per the assignment's
      own wording — or (b) adding a direct Anthropic API call as the real
      model path instead, using Secrets Manager (supported) to hold the
      API key. Option (b) needs an Anthropic API key.
- [ ] Pin the deploy region to `us-east-1` in `scripts/deploy.sh` / SAM
      config.
- [ ] Get temporary credentials from **AWS Details → AWS CLI** into
      `~/.aws/credentials`.
- [ ] `export LAB_ROLE_ARN=$(aws iam get-role --role-name LabRole --query Role.Arn --output text)`
- [ ] Run `./scripts/deploy.sh` and confirm the stack comes up.
- [ ] Hit the deployed `/ask` endpoint and confirm you get a response
      (stub or live).
- [ ] Update `docs/ARCHITECTURE.md` with whichever outcome is real for
      this account — don't leave the narrative describing a component
      that turned out to be unavailable.
- [ ] Fill in `docs/PROVENANCE.md` with actual review notes once the
      above is done.
- [ ] Watch the budget banner; `sam delete --stack-name
      ai-cloud-qa-starter` when done for the day, per the Lab's own
      recommendation for CloudFormation-managed resources.
