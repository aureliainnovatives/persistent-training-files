# Medallion Architecture --- Integration Architect Classroom Notes

## 1. Core Idea

**Medallion Architecture** organizes data into progressively refined
layers.

``` text
SOURCE SYSTEMS
      |
      v
+------------------+
|      BRONZE      |
| Raw / Landed     |
+------------------+
      |
      v
+------------------+
|      SILVER      |
| Clean / Trusted  |
+------------------+
      |
      v
+------------------+
|       GOLD       |
| Business / Serve |
+------------------+
      |
      v
BI | Analytics | ML/AI | APIs
```

> **Bronze preserves what arrived, Silver makes it trustworthy, and Gold
> makes it useful to the business.**

## 2. Why Do We Need It?

Without clear layers, ingestion, cleansing, business rules and reporting
logic often become mixed together.

``` text
WITHOUT LAYERS

CRM --------\
ERP ---------> Large ETL / Transformation ---> Reports
Files ------/              |
APIs ---------------------/
                           |
                     Hard to debug
                     Hard to replay
                     Hard to govern
                     Hard to reuse
```

Medallion separates responsibilities:

``` text
INGEST              REFINE              SERVE
  |                   |                   |
  v                   v                   v
BRONZE ------------> SILVER -----------> GOLD
raw                   trusted             business-ready
```

## 3. Bronze --- Raw / Landed Data

**Purpose:** Capture source data with minimal transformation.

Typical sources: - SAP / ERP - CRM - Databases - REST APIs - Files -
Kafka / events - IoT / SaaS

``` text
SAP --------\
CRM ---------\
REST API -----> [ BRONZE ]
Files -------/     RAW
Kafka ------/
```

Typical characteristics: - Preserve source fidelity - Keep history where
required - Add ingestion metadata - Enable replay/reprocessing - Avoid
complex business rules

**Architect question:** If tomorrow our transformation logic is wrong,
can we rebuild downstream data without asking every source to resend it?

## 4. Silver --- Clean / Trusted Data

**Purpose:** Clean, validate, standardize and integrate data.

``` text
                 BRONZE
                    |
                    v
             +-------------+
             |   SILVER    |
             +-------------+
              /    |     \
             v     v      v
           Clean Validate Join
              \    |     /
               +---+----+
                   |
              TRUSTED DATA
```

Typical operations: - Type conversion - Null handling - Deduplication -
Standardization - Schema validation - Data-quality rules - Joining
datasets - Master/reference-data enrichment

Example:

``` text
BRONZE
abc retail
ABC Retail Ltd.
ABC RETAIL
      |
      | standardize
      v
SILVER
customer_id: C1001
customer_name: ABC Retail
```

> Silver should represent **reusable trusted data**, not one dashboard's
> presentation logic.

## 5. Gold --- Business / Serving Data

**Purpose:** Prepare data for business consumption.

``` text
                   SILVER
                     |
        +------------+-------------+
        |            |             |
        v            v             v
   Sales Gold   Finance Gold   Customer Gold
        |            |             |
        v            v             v
       BI          Reports       AI / ML
```

Gold may contain: - KPIs - Aggregations - Business metrics - Dimensional
models - Reporting tables - Feature datasets - Domain-specific serving
models

Example:

``` text
Silver Orders
     +
Silver Customers
     +
Silver Products
     |
     v
GOLD: Daily Sales by Region

date | region | revenue | orders | avg_order_value
```

## 6. End-to-End Example

``` text
       SAP Orders          Salesforce Customers
            |                       |
            +-----------+-----------+
                        |
                        v
                   +---------+
                   | BRONZE  |
                   | raw     |
                   +----+----+
                        |
                        v
                   +---------+
                   | SILVER  |
                   | clean   |
                   | validate|
                   | join    |
                   +----+----+
                        |
                        v
                   +---------+
                   |  GOLD   |
                   | KPI     |
                   | C360    |
                   | Revenue |
                   +----+----+
                        |
               +--------+--------+
               |        |        |
               v        v        v
              BI       ML/AI    APIs
```

## 7. Where ETL / ELT Fits

Medallion is an **architecture pattern**. ETL/ELT describes **how data
moves and transforms**.

``` text
SOURCE
   |
   | Extract + Load
   v
BRONZE
   |
   | Transform
   v
SILVER
   |
   | Transform / Aggregate
   v
GOLD
```

Modern lakehouse platforms often favor an ELT-style approach:

``` text
Extract -> Load raw data -> Transform inside the platform
```

Architectural question:

> Where does transformation happen, who owns it, how is it governed, and
> can we replay it?

## 8. Data Lake vs Warehouse vs Lakehouse

``` text
DATA LAKE
Flexible, large-scale storage
Structured + semi/unstructured data
              \
               \
                +----> LAKEHOUSE
               /
              /
DATA WAREHOUSE
Structured, governed, SQL/BI optimized
```

A Lakehouse aims to combine lake flexibility with warehouse-style
management and analytics capabilities.

``` text
              LAKEHOUSE
                  |
       +----------+----------+
       |          |          |
       v          v          v
      BI        Data       AI / ML
              Engineering
```

## 9. Where Databricks Fits

Databricks can implement this architecture using lakehouse capabilities.

``` text
                    DATABRICKS
                        |
       +----------------+----------------+
       |                |                |
       v                v                v
   Ingestion       Processing       Governance
       |                |                |
       +----------------+----------------+
                        |
                        v
                 Delta / Lakehouse
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       BRONZE         SILVER         GOLD
```

Concepts worth introducing: - Delta Lake - Unity Catalog - Apache
Spark - SQL Warehouses - Jobs / Workflows - Batch and Streaming - Data
Engineering - ML / AI workloads

**Important:** Bronze, Silver and Gold are logical architectural layers,
not Databricks products.

## 10. Batch + Streaming

``` text
BATCH SOURCES ------------------\
                                 > BRONZE -> SILVER -> GOLD
STREAMING SOURCES --------------/
```

The pattern is not restricted to batch pipelines.

## 11. Governance and Data Quality

Do not present Medallion as merely three folders.

``` text
                 GOVERNANCE
                     |
        +------------+------------+
        |            |            |
        v            v            v
     BRONZE        SILVER        GOLD
        |            |            |
     metadata      quality      business
     lineage       validation   definitions
     access        schema       access
```

Cross-cutting concerns: - Ownership - Lineage - Schema evolution -
Access control - PII handling - Data quality - Retention -
Auditability - Observability

## 12. Integration Architect View

Ask at every boundary:

``` text
SOURCE
  |
  | How do we ingest?
  v
BRONZE
  |
  | How do we validate, reconcile and standardize?
  v
SILVER
  |
  | Which business rules and serving models are required?
  v
GOLD
  |
  | Who consumes it and under what SLA?
  v
CONSUMER
```

And think horizontally:

``` text
Security | Governance | Quality | Lineage | Observability

SOURCE ------> BRONZE ------> SILVER ------> GOLD ------> CONSUMER
```

## 13. Common Misconceptions

**Bronze means bad data.**\
No. It means data close to the source, before downstream refinement.

**Everything must have exactly three physical layers.**\
No. Bronze/Silver/Gold is a logical pattern. Real systems may add
staging, quarantine, semantic or serving layers.

**Gold always means aggregated data.**\
No. Gold is consumption-oriented; aggregation is common but not
mandatory.

**Medallion Architecture means Databricks.**\
No. It is an architecture pattern. Databricks strongly supports and
popularized it, but the idea is broader than one platform.

## 14. Five-Minute Whiteboard Story

Draw this first:

``` text
SAP      Salesforce      Files
 |           |             |
 +-----------+-------------+
             |
             v
          BRONZE
             |
             v
          SILVER
             |
             v
           GOLD
             |
       +-----+-----+
       |     |     |
       BI    AI   API
```

Ask:

**Why not transform everything before Bronze?**

Lead toward: - Source fidelity - Replay - Audit - Debugging - Changing
transformation rules

Then ask:

**Why not let every dashboard directly consume Bronze?**

Lead toward: - Inconsistent definitions - Data quality - Repeated
transformations - Governance - Reusability

Finish with:

> **Bronze gives recoverability. Silver gives trust. Gold gives business
> usability.**

## 15. Summary

``` text
BRONZE
Raw / historical / replayable
          |
          v
SILVER
Clean / validated / integrated / reusable
          |
          v
GOLD
Business-ready / consumption-oriented
          |
          v
BI | Analytics | ML | AI | APIs
```

**Medallion Architecture is less about naming three storage locations
and more about establishing clear stages of data quality, responsibility
and consumption.**
