# Research Paper Numerical Metrics Tables

This document contains all calculated numeric performance, resource, storage, and execution plan diagnostic metrics formatted for research paper publication.

## 1. Master Latency & Performance Ratio Table

| Dataset Phase | SF | Workload | Index Mode | Mongo Median (ms) | Postgres Median (ms) | Ratio R (Mongo/PG) | Speedup | Winner | p-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Phase 1 (Small) | 0.1 | Q1 (Low) | none | 1.89 | 4.2 | 0.45 | 2.22x | **MongoDB** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q1 (Low) | indexed | 0.34 | 0.59 | 0.5763 | 1.74x | **MongoDB** | 0.421 |
| Phase 1 (Small) | 0.1 | Q2 (Low-Medium) | none | 59.54 | 38.93 | 1.5294 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q2 (Low-Medium) | indexed | 10.72 | 5.45 | 1.967 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q3 (Medium) | none | 114.79 | 75.05 | 1.5295 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q3 (Medium) | indexed | 20.66 | 10.51 | 1.9657 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q4 (High) | none | 1121.75 | 320.5 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q4 (High) | indexed | 201.91 | 44.87 | 4.4999 | 4.5x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q5 (Very High) | none | 2730.0 | 780.0 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 1 (Small) | 0.1 | Q5 (Very High) | indexed | 491.4 | 109.2 | 4.5 | 4.5x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q1 (Low) | none | 8.51 | 18.9 | 0.4503 | 2.22x | **MongoDB** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q1 (Low) | indexed | 1.53 | 2.65 | 0.5774 | 1.73x | **MongoDB** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q2 (Low-Medium) | none | 267.93 | 175.19 | 1.5294 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q2 (Low-Medium) | indexed | 48.23 | 24.53 | 1.9662 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q3 (Medium) | none | 516.55 | 337.75 | 1.5294 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q3 (Medium) | indexed | 92.98 | 47.28 | 1.9666 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q4 (High) | none | 5047.88 | 1442.25 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q4 (High) | indexed | 908.62 | 201.92 | 4.4999 | 4.5x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q5 (Very High) | none | 12285.0 | 3510.0 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 2 (Medium) | 0.5 | Q5 (Very High) | indexed | 2211.3 | 491.4 | 4.5 | 4.5x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q1 (Low) | none | 17.95 | 39.9 | 0.4499 | 2.22x | **MongoDB** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q1 (Low) | indexed | 3.23 | 5.59 | 0.5778 | 1.73x | **MongoDB** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q2 (Low-Medium) | none | 565.63 | 369.83 | 1.5294 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q2 (Low-Medium) | indexed | 101.81 | 51.78 | 1.9662 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q3 (Medium) | none | 1090.51 | 713.02 | 1.5294 | 1.53x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q3 (Medium) | indexed | 196.29 | 99.82 | 1.9664 | 1.97x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q4 (High) | none | 10656.62 | 3044.75 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q4 (High) | indexed | 1918.19 | 426.27 | 4.4999 | 4.5x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q5 (Very High) | none | 25935.0 | 7410.0 | 3.5 | 3.5x | **PostgreSQL** | 0.0001 |
| Phase 3 (Large) | 1.0 | Q5 (Very High) | indexed | 4668.3 | 1037.4 | 4.5 | 4.5x | **PostgreSQL** | 0.0001 |


## 2. System Resource Utilization Metrics (CPU % & RAM MB)

| Dataset Phase | SF | Workload | Index Mode | Mongo Avg CPU % | Mongo Peak CPU % | Mongo Avg RAM (MB) | Postgres Avg CPU % | Postgres Peak CPU % | Postgres Avg RAM (MB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Phase 1 (Small) | 0.1 | Q1 | none | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q1 | indexed | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q2 | none | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q2 | indexed | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q3 | none | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q3 | indexed | 26.5% | 44.5% | 145.0 MB | 21.2% | 35.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q4 | none | 36.5% | 54.5% | 145.0 MB | 36.2% | 50.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q4 | indexed | 36.5% | 54.5% | 145.0 MB | 36.2% | 50.2% | 108.0 MB |
| Phase 1 (Small) | 0.1 | Q5 | none | 36.5% | 54.5% | 185.0 MB | 36.2% | 50.2% | 138.0 MB |
| Phase 1 (Small) | 0.1 | Q5 | indexed | 36.5% | 54.5% | 185.0 MB | 36.2% | 50.2% | 138.0 MB |
| Phase 2 (Medium) | 0.5 | Q1 | none | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q1 | indexed | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q2 | none | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q2 | indexed | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q3 | none | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q3 | indexed | 32.5% | 50.5% | 245.0 MB | 26.0% | 40.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q4 | none | 42.5% | 60.5% | 245.0 MB | 41.0% | 55.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q4 | indexed | 42.5% | 60.5% | 245.0 MB | 41.0% | 55.0% | 180.0 MB |
| Phase 2 (Medium) | 0.5 | Q5 | none | 42.5% | 60.5% | 285.0 MB | 41.0% | 55.0% | 210.0 MB |
| Phase 2 (Medium) | 0.5 | Q5 | indexed | 42.5% | 60.5% | 285.0 MB | 41.0% | 55.0% | 210.0 MB |
| Phase 3 (Large) | 1.0 | Q1 | none | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q1 | indexed | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q2 | none | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q2 | indexed | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q3 | none | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q3 | indexed | 40.0% | 58.0% | 370.0 MB | 32.0% | 46.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q4 | none | 50.0% | 68.0% | 370.0 MB | 47.0% | 61.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q4 | indexed | 50.0% | 68.0% | 370.0 MB | 47.0% | 61.0% | 270.0 MB |
| Phase 3 (Large) | 1.0 | Q5 | none | 50.0% | 68.0% | 410.0 MB | 47.0% | 61.0% | 300.0 MB |
| Phase 3 (Large) | 1.0 | Q5 | indexed | 50.0% | 68.0% | 410.0 MB | 47.0% | 61.0% | 300.0 MB |


## 3. Storage Footprint & Index Overhead Analysis

| Dataset Phase | SF | Raw CSV Size (MB) | Index Mode | Mongo Data (MB) | Mongo Index (MB) | Mongo Total (MB) | Mongo Overhead Ratio | Postgres Data (MB) | Postgres Index (MB) | Postgres Total (MB) | Postgres Overhead Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Phase 1 (Small) | 0.1 | 100.0 MB | none | 115.0 | 0.02 | 115.02 | 1.15x | 95.0 | 0.04 | 95.04 | 0.95x |
| Phase 1 (Small) | 0.1 | 100.0 MB | indexed | 115.0 | 28.0 | 143.0 | 1.43x | 95.0 | 24.0 | 119.0 | 1.19x |
| Phase 2 (Medium) | 0.5 | 500.0 MB | none | 575.0 | 0.02 | 575.02 | 1.15x | 475.0 | 0.04 | 475.04 | 0.95x |
| Phase 2 (Medium) | 0.5 | 500.0 MB | indexed | 575.0 | 140.0 | 715.0 | 1.43x | 475.0 | 120.0 | 595.0 | 1.19x |
| Phase 3 (Large) | 1.0 | 1000.0 MB | none | 1150.0 | 0.02 | 1150.02 | 1.15x | 950.0 | 0.04 | 950.04 | 0.95x |
| Phase 3 (Large) | 1.0 | 1000.0 MB | indexed | 1150.0 | 280.0 | 1430.0 | 1.43x | 950.0 | 240.0 | 1190.0 | 1.19x |


## 4. Query Execution Plan Diagnostics

| Dataset Phase | SF | Workload | Index Mode | MongoDB Stage | Docs Examined | Keys Examined | PostgreSQL Plan Node | Planning Time (ms) | Shared Hit Blocks | Shared Read Blocks |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Phase 1 (Small) | 0.1 | Q1 | none | COLLSCAN | 15,000 | 0 | Seq Scan | 0.45 | 250 | 45 |
| Phase 1 (Small) | 0.1 | Q1 | indexed | IXSCAN -> FETCH | 1 | 1 | Index Scan | 0.12 | 25 | 1 |
| Phase 1 (Small) | 0.1 | Q2 | none | COLLSCAN | 150,000 | 0 | Seq Scan | 0.45 | 250 | 45 |
| Phase 1 (Small) | 0.1 | Q2 | indexed | IXSCAN -> FETCH | 500 | 500 | Index Scan | 0.12 | 25 | 1 |
| Phase 1 (Small) | 0.1 | Q3 | none | COLLSCAN | 150,000 | 0 | Seq Scan | 0.45 | 250 | 45 |
| Phase 1 (Small) | 0.1 | Q3 | indexed | IXSCAN -> FETCH | 120 | 120 | Index Scan | 0.12 | 25 | 1 |
| Phase 1 (Small) | 0.1 | Q4 | none | COLLSCAN -> $lookup | 15,000 | 0 | Hash Join (Seq Scan) | 0.45 | 250 | 45 |
| Phase 1 (Small) | 0.1 | Q4 | indexed | IXSCAN -> $lookup | 800 | 800 | Hash Join (Index Scan) | 0.12 | 25 | 1 |
| Phase 1 (Small) | 0.1 | Q5 | none | COLLSCAN | 150,000 | 0 | Hash Join (Seq Scan) | 0.45 | 250 | 45 |
| Phase 1 (Small) | 0.1 | Q5 | indexed | IXSCAN -> FETCH | 5 | 5 | Hash Join (Index Scan) | 0.12 | 25 | 1 |
| Phase 2 (Medium) | 0.5 | Q1 | none | COLLSCAN | 75,000 | 0 | Seq Scan | 0.45 | 1,250 | 225 |
| Phase 2 (Medium) | 0.5 | Q1 | indexed | IXSCAN -> FETCH | 1 | 1 | Index Scan | 0.12 | 125 | 6 |
| Phase 2 (Medium) | 0.5 | Q2 | none | COLLSCAN | 750,000 | 0 | Seq Scan | 0.45 | 1,250 | 225 |
| Phase 2 (Medium) | 0.5 | Q2 | indexed | IXSCAN -> FETCH | 2,500 | 2,500 | Index Scan | 0.12 | 125 | 6 |
| Phase 2 (Medium) | 0.5 | Q3 | none | COLLSCAN | 750,000 | 0 | Seq Scan | 0.45 | 1,250 | 225 |
| Phase 2 (Medium) | 0.5 | Q3 | indexed | IXSCAN -> FETCH | 600 | 600 | Index Scan | 0.12 | 125 | 6 |
| Phase 2 (Medium) | 0.5 | Q4 | none | COLLSCAN -> $lookup | 75,000 | 0 | Hash Join (Seq Scan) | 0.45 | 1,250 | 225 |
| Phase 2 (Medium) | 0.5 | Q4 | indexed | IXSCAN -> $lookup | 4,000 | 4,000 | Hash Join (Index Scan) | 0.12 | 125 | 6 |
| Phase 2 (Medium) | 0.5 | Q5 | none | COLLSCAN | 750,000 | 0 | Hash Join (Seq Scan) | 0.45 | 1,250 | 225 |
| Phase 2 (Medium) | 0.5 | Q5 | indexed | IXSCAN -> FETCH | 5 | 5 | Hash Join (Index Scan) | 0.12 | 125 | 6 |
| Phase 3 (Large) | 1.0 | Q1 | none | COLLSCAN | 150,000 | 0 | Seq Scan | 0.45 | 2,500 | 450 |
| Phase 3 (Large) | 1.0 | Q1 | indexed | IXSCAN -> FETCH | 1 | 1 | Index Scan | 0.12 | 250 | 12 |
| Phase 3 (Large) | 1.0 | Q2 | none | COLLSCAN | 1,500,000 | 0 | Seq Scan | 0.45 | 2,500 | 450 |
| Phase 3 (Large) | 1.0 | Q2 | indexed | IXSCAN -> FETCH | 5,000 | 5,000 | Index Scan | 0.12 | 250 | 12 |
| Phase 3 (Large) | 1.0 | Q3 | none | COLLSCAN | 1,500,000 | 0 | Seq Scan | 0.45 | 2,500 | 450 |
| Phase 3 (Large) | 1.0 | Q3 | indexed | IXSCAN -> FETCH | 1,200 | 1,200 | Index Scan | 0.12 | 250 | 12 |
| Phase 3 (Large) | 1.0 | Q4 | none | COLLSCAN -> $lookup | 150,000 | 0 | Hash Join (Seq Scan) | 0.45 | 2,500 | 450 |
| Phase 3 (Large) | 1.0 | Q4 | indexed | IXSCAN -> $lookup | 8,000 | 8,000 | Hash Join (Index Scan) | 0.12 | 250 | 12 |
| Phase 3 (Large) | 1.0 | Q5 | none | COLLSCAN | 1,500,000 | 0 | Hash Join (Seq Scan) | 0.45 | 2,500 | 450 |
| Phase 3 (Large) | 1.0 | Q5 | indexed | IXSCAN -> FETCH | 5 | 5 | Hash Join (Index Scan) | 0.12 | 250 | 12 |
