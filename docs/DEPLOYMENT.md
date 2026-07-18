# Deploying to the AWS Academy Learner Lab

Two ways to deploy this prototype into the Lab sandbox. `scripts/deploy.sh`
pins the region to `us-east-1` by default (override with `AWS_REGION`),
matching the Lab's region restriction.

## Option A: AWS CloudShell (recommended — nothing to install locally)

CloudShell runs inside the Lab console and already has AWS CLI + credentials
configured for the Lab account.

1. **Start Lab** → open the **AWS** console link → click the **CloudShell**
   icon (top toolbar).
2. Confirm the region selector (top right) is set to **US East (N.
   Virginia) / us-east-1**.
3. Clone the repo (it's public, no auth needed):
   ```bash
   git clone https://github.com/asligulcur/AI-Cloud-AWS.git
   cd AI-Cloud-AWS
   ```
4. Install SAM CLI (CloudShell has Python/pip but not SAM by default):
   ```bash
   pip install --user aws-sam-cli
   export PATH="$HOME/.local/bin:$PATH"
   ```
5. Get the LabRole ARN and deploy:
   ```bash
   export LAB_ROLE_ARN=$(aws iam get-role --role-name LabRole --query Role.Arn --output text)
   ./scripts/deploy.sh
   ```
6. When it finishes, `sam deploy` prints an **Outputs** section with
   `ApiUrl`. Test it:
   ```bash
   curl -X POST "<ApiUrl-from-output>" -H "Content-Type: application/json" -d '{"question":"What is S3?"}'
   ```
   You should get back a JSON response — `"source": "stub"` unless Bedrock
   access is confirmed working (see
   [`LEARNER_LAB_REVIEW.md`](LEARNER_LAB_REVIEW.md)).

## Option B: Locally (or in the devcontainer), against the Lab account

Install the tooling first:

```bash
pip install -r requirements-dev.txt   # installs aws-sam-cli, boto3
```

Then:

1. In the Lab, click **AWS Details** → copy the **AWS CLI** credentials
   block (Access Key ID, Secret Access Key, Session Token).
2. Paste them into `~/.aws/credentials` as a `[default]` profile (they're
   temporary — expire when the session ends).
3. Run the same commands as step 5–6 above:
   ```bash
   export LAB_ROLE_ARN=$(aws iam get-role --role-name LabRole --query Role.Arn --output text)
   ./scripts/deploy.sh
   ```

CloudShell is less fiddly since there's no credential-copying step and no
risk of stale/expired keys sitting in `~/.aws/credentials` after the
session ends — start there if unsure.

## Before deploying: stub vs. live

Decide whether to attempt live Bedrock now, or deploy stub-only first to
confirm the pipeline works end-to-end, and tackle Bedrock/Anthropic
separately. Either is fine — the stack deploys and runs the same either
way, since the stub fallback is automatic. See
[`LEARNER_LAB_REVIEW.md`](LEARNER_LAB_REVIEW.md) for the open question on
Bedrock availability in this account.

## Tearing down

Everything here is pay-per-request, but it's still good practice to remove
the stack when you're done for the day/term:

```bash
sam delete --stack-name ai-cloud-qa-starter --region us-east-1
```
