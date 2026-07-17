#!/usr/bin/env bash
# Build and deploy the prototype into the AWS Academy Learner Lab sandbox.
#
# Prereqs:
#   1. Start your Learner Lab session and copy the temporary credentials
#      (AWS Details > AWS CLI) into ~/.aws/credentials or export them as
#      AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN.
#   2. Find your LabRole ARN: aws iam get-role --role-name LabRole
#   3. Enable model access for the Bedrock model in the Bedrock console
#      (Model access page) if you want live (non-stub) answers.
set -euo pipefail

cd "$(dirname "$0")/.."

LAB_ROLE_ARN="${LAB_ROLE_ARN:-}"
if [[ -z "$LAB_ROLE_ARN" ]]; then
  echo "Set LAB_ROLE_ARN to your Learner Lab role ARN first, e.g.:" >&2
  echo '  export LAB_ROLE_ARN=$(aws iam get-role --role-name LabRole --query Role.Arn --output text)' >&2
  exit 1
fi

sam build --template-file infra/template.yaml

sam deploy \
  --stack-name ai-cloud-qa-starter \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "LabRoleArn=${LAB_ROLE_ARN}" \
  --no-confirm-changeset
