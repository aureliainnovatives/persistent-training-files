# Runbook — High Application Latency
1. Establish affected service, incident time, p95/p99 latency, error rate and request rate.
2. Check CPU, memory, desired/running tasks and target health. Do not assume high latency means insufficient compute.
3. Search logs for DB timeouts, connection acquisition failures, dependency failures and exceptions.
4. Correlate deployments/configuration changes immediately preceding the incident.
5. For each hypothesis record supporting evidence, contradicting evidence and missing evidence.
6. Prefer the lowest-risk reversible remediation supported by evidence.
Production rollback, restart, scaling or configuration mutation requires change approval.
After remediation verify p95, 5xx, task health and dependency errors.
