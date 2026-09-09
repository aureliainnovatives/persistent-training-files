# Runbook — Database Connection Pool Exhaustion
## Symptoms
Connection acquisition timeout, DB timeout, high API latency and elevated 5xx. CPU/memory may remain normal.
## Investigation
1. Confirm ECS tasks are healthy.
2. Compare latency/error rate with baseline.
3. Search logs for connection acquisition errors.
4. Inspect recent deployment/configuration changes.
5. Compare current pool configuration with last known good configuration.
6. Check whether traffic materially increased.
## Checkout API reference
Normal production maximum connection-pool size: **80**.
## Remediation
If exhaustion begins immediately after a deployment that changed pool configuration, establish correlation, prepare rollback, obtain human approval, execute only the approved change, then monitor latency, 5xx, task health and DB connectivity.
Never autonomously rollback production without approval.
