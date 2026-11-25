# Data Engineering Projects

A portfolio of hands-on data engineering projects covering pipeline orchestration, containerised infrastructure, SQL development, and data modelling.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?logo=duckdb&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?logo=dbt&logoColor=white)

## Projects

| # | Project | Description | Tech Stack | Status |
|---|---------|-------------|------------|--------|
| 01 | [Custom ELT Project](./01-custom-elt-project) | End-to-end ELT pipeline: Python copies data between two containerised Postgres databases, dbt transforms it, and Airflow orchestrates the run. | Python, PostgreSQL, Docker, Apache Airflow, dbt | ✅ Completed |
| 02 | [SQL Data Engineering Projects](./02-sql-data-engineering-projects) | A collection of SQL-based exercises and implementations focused on database development, data modelling, and data transformation. | SQL, DuckDB | ✅ Completed |

---

### 01. Custom ELT Project

An end-to-end ELT pipeline: Python copies data between two containerised Postgres databases, dbt transforms it, and Airflow orchestrates the run. Based on freeCodeCamp.org's *Data Engineering Course for Beginners*, rebuilt with current tool versions.

- **Technologies:** Python, PostgreSQL, Docker, Apache Airflow, dbt
- **Status:** ✅ Completed. Possible extensions (API source, incremental loading, CI/CD) are listed in the project's roadmap.

[View Project →](./01-custom-elt-project)

### 02. SQL Data Engineering Projects

A collection of SQL-based data engineering exercises and implementations focused on database development, data modelling, and data transformation.

- **Technologies:** SQL, DuckDB
- **Status:** ✅ Completed

[View Project →](./02-sql-data-engineering-projects)

---

## Repository Structure

```text
data-engineering-projects/
├── 01-custom-elt-project/              # ELT pipeline (Airflow, dbt, Docker)
│   ├── figure/                         # Screenshots and architecture diagram
│   └── README.md
├── 02-sql-data-engineering-projects/   # SQL projects
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

Each project is self-contained and has its own README with setup instructions, prerequisites, and usage details.

```bash
git clone https://github.com/<your-username>/data-engineering-projects.git
cd data-engineering-projects
```

Then open the folder of the project you're interested in and follow its README.

Project 01 runs in Docker, so it needs Docker with Docker Compose and at least 4 GB of memory allocated to Docker.

## Tech Stack Overview

| Area | Tools |
|------|-------|
| Languages | Python, SQL |
| Databases | PostgreSQL, DuckDB |
| Orchestration | Apache Airflow |
| Transformation | dbt |
| Infrastructure | Docker |

## Roadmap

- [x] Complete Project 01 (Custom ELT Project)
- [x] Add architecture diagram to Project 01
- [ ] Extend Project 01: API source, incremental loading, cloud warehouse
- [ ] Add data quality tests and CI checks