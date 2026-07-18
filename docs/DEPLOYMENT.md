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
   If this fails with a Python-version error (`PythonPipBuilder:Validation`),
   CloudShell's local Python doesn't match the runtime pinned in
   `infra/template.yaml` — see [`LEARNER_LAB_REVIEW.md`](LEARNER_LAB_REVIEW.md)
   for the fix (bumping the template's `Runtime` to match what's actually
   on CloudShell's PATH).
6. When it finishes, `sam deploy` prints an **Outputs** section with
   `ApiUrl`. Test it:
   ```bash
   curl -X POST "<ApiUrl-from-output>" -H "Content-Type: application/json" -d '{"question":"What is S3?"}'
   ```
   You should get back a JSON response — `"source": "stub"` unless Bedrock
   access is confirmed working (see
   [`LEARNER_LAB_REVIEW.md`](LEARNER_LAB_REVIEW.md)).
7. To see the actual frontend (not just curl), point `frontend/index.html`'s
   `API_URL` at your `ApiUrl` output, then serve it locally rather than
   opening the file directly — Safari blocks `fetch()` from a bare `file://`
   page:
   ```bash
   cd frontend && python3 -m http.server 8000
   # open http://localhost:8000/index.html
   ```
   CORS is already enabled on the API (`infra/template.yaml`'s
   `HttpApi.CorsConfiguration`) specifically so this works from a browser.

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

## Current status: stub vs. live

The team's live deployment has been verified end-to-end (via `curl` and
the actual frontend in a browser) and currently runs **stub-only** —
Bedrock's `InvokeModel` call fails over to the stub path in this account,
consistent with Bedrock not appearing in the Lab's supported-services
list. See [`LEARNER_LAB_REVIEW.md`](LEARNER_LAB_REVIEW.md) for the full
finding. Going live (via Bedrock model access, or a direct Anthropic API
call instead) is a deliberate follow-up, not a blocker.

## Tearing down

Everything here is pay-per-request, but it's still good practice to remove
the stack when you're done for the day/term:

```bash
sam delete --stack-name ai-cloud-qa-starter --region us-east-1
```
