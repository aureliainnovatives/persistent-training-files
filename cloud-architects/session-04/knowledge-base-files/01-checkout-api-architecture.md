# Checkout API — Production Architecture
## Service purpose
`checkout-api` is the customer-facing checkout orchestration service.
## AWS deployment
- Region: ap-south-1
- Compute: Amazon ECS
- Desired tasks: 6
- Load balancer: ALB
- Database: Amazon RDS PostgreSQL
- Observability: CloudWatch metrics and logs
## Normal baseline
| Signal | Normal |
|---|---|
| CPU | 35–55% |
| Memory | 45–70% |
| p95 latency | <350 ms |
| HTTP 5xx | <1% |
| Healthy ECS tasks | 6 |
## Database dependency
The normal production DB connection-pool maximum is **80**. Pool exhaustion can cause latency and 5xx while CPU, memory, and ECS health remain normal.
## Governance
Production changes require approval.
