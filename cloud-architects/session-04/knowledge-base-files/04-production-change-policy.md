# Production Change and Agent Action Policy
## Allowed read-only actions
Read metrics/logs, inspect ECS/EC2 health, deployment history and CloudTrail, retrieve runbooks, prepare recommendations/change proposals.
## Explicit human approval required
Restart/scale production, modify IAM/security groups/database configuration, rollback deployments, terminate resources, or modify routing/load balancers.
## Critical principle
A prompt saying "do not make unauthorized changes" is not an authorization control. Authorization must be enforced by the application/tool/API/IAM layer.
## Audit
Record incident/change ID, approver, approved action/resource, timestamp and outcome. Validate after every change.
