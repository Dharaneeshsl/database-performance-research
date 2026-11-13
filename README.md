# Database Performance Research: MongoDB vs PostgreSQL (TPC-H Benchmark)

An experimental analysis of **MongoDB** and **PostgreSQL** performance under varying data volumes, query complexities, and indexing strategies using TPC-H workloads.

## Final submission files

- `main.tex`: final manuscript source, with its original section structure and supplied numerical results.
- `main.pdf`: final 10-page exported paper.
- `figures/`: the 14 final figures; Figures 1 and 2 are black and white.
- `outputs/evidence/`: summary CSVs used by the final chart generator.
- `outputs/evidence/verification-run/`: earlier verification logs, kept separately with their provenance limitation.

The manuscript values were supplied by the author from Antigravity; this repository does not certify that every value was independently reproduced. Older `results/processed/` outputs and legacy analysis scripts are retained for project history and are not the authoritative final submission tables.

To regenerate the final charts, run `python -m analysis.publication_figures`. Local database files, generated datasets, downloads, and temporary work are excluded from Git. Copy `config/database.example.yaml` to `config/database.yaml` and enter credentials locally.

## Research Questions
- **RQ1 (Data Volume)**: How does increasing data volume affect CRUD performance in MongoDB and PostgreSQL?
- **RQ2 (Query Complexity)**: How does query complexity (Q1–Q5) affect query response times?
- **RQ3 (Indexing)**: What is the impact of indexing on read latency versus storage and write maintenance cost?
- **RQ4 (Resource Usage)**: How do storage, CPU utilization, and RAM consumption scale across database engines?
- **RQ5 (Workload Suitability)**: Under what workload characteristics does MongoDB outperform PostgreSQL, and vice versa?

---

## Directory Structure

```
database-performance-study/
│
├── config/                  # Master configuration YAML files
│   ├── experiment.yaml      # Benchmark parameters (Scale factors, repetitions)
│   └── database.yaml        # Connection strings and credentials
│
├── data/                    # TPC-H raw and processed datasets
│   ├── raw/                 # Generated raw CSV/TBL data
│   └── processed/           # Validated data files
│
├── schemas/                 # Database schema definitions
│   ├── postgresql/schema.sql# PostgreSQL DDL script
│   └── mongodb/schema.py    # MongoDB collection and index definitions
│
├── loaders/                 # Data generation and bulk insertion scripts
│   ├── generator.py         # Pure-Python TPC-H data generator
│   ├── postgres_loader.py   # PostgreSQL COPY bulk loader
│   ├── mongo_loader.py      # PyMongo insert_many bulk loader
│   └── validate.py          # Row/Document validation checker
│
├── workloads/               # Workload query definitions
│   ├── crud.py              # Insert, Read, Update, Delete workloads
│   ├── q1_simple.py         # Q1: Equality lookup
│   ├── q2_range.py          # Q2: Range query
│   ├── q3_multi_condition.py# Q3: Multi-condition query
│   ├── q4_join.py           # Q4: Relational join query ($lookup / JOIN)
│   └── q5_aggregation.py    # Q5: Complex aggregation query ($lookup + $group / JOIN + GROUP BY)
│
├── benchmark/               # Benchmarking framework
│   ├── timer.py             # High-resolution perf_counter timer
│   ├── metrics.py           # Metrics calculation utilities
│   ├── system_monitor.py    # CPU and RAM background sampling daemon
│   ├── database_reset.py    # Automated database clean and re-hydrate pipeline
│   ├── runner.py            # Single workload runner
│   └── experiment_manager.py# Master experiment matrix runner
│
├── explain/                 # Diagnostics and Query Execution Plan extraction
│   ├── mongo_explain.py     # MongoDB explain("executionStats") parser
│   └── postgres_explain.py  # PostgreSQL EXPLAIN (ANALYZE, BUFFERS) parser
│
├── analysis/                # Statistical analysis and visualization
│   ├── statistics.py        # Summary statistics calculation (mean, median, p95, p99, std)
│   └── plots.py             # 12 high-resolution paper visualization figures generator
│
├── results/                 # Measurement outputs
│   ├── raw/                 # Untouched raw CSV measurement logs
│   ├── processed/           # Summary statistical tables
│   └── figures/             # 300 DPI publication plots
│
└── paper/                   # Final research manuscript artifacts
    ├── manuscript.md        # Comprehensive Markdown research paper
    ├── manuscript.docx      # Formatted Word paper artifact
    └── figures/             # Included paper graphics
```

---

## Quick Start & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Configuration
Copy `config/database.example.yaml` to `config/database.yaml`, then enter your local PostgreSQL and MongoDB credentials. This local file is ignored by Git.

### 3. Generate TPC-H Data
```bash
python -m loaders.generator --scale-factor 0.1
```

### 4. Validate Loaded Data
```bash
python -m loaders.validate
```

### 5. Run Full Benchmark Pipeline
```bash
python -m benchmark.experiment_manager
```

### 6. Analyze Results & Generate Plots
```bash
python -m analysis.statistics
python -m analysis.plots
```
