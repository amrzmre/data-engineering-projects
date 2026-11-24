# 01. Custom ELT Project

An end-to-end ELT pipeline: Python copies data between two containerised Postgres databases, dbt transforms it, and Airflow orchestrates the run.

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Extract and load script |
| **PostgreSQL 18** | Source and destination databases |
| **Docker / Docker Compose** | Containerised services |
| **dbt (dbt-core 1.11 + dbt-postgres 1.11)** | SQL-based transformations and tests |
| **Apache Airflow 3.3** | Workflow orchestration (LocalExecutor) |

## Architecture

```text
Source DB (Postgres)  →  ELT script (Python)  →  Destination DB (Postgres)  →  dbt models
        ▲                  pg_dump → psql          schema: public (raw copy)    schema: analytics
   init.sql seeds

        Airflow DAG `elt_pipeline`:  elt_copy  →  dbt_build
```

Airflow runs both steps inside its own custom image (which contains the Postgres client, the ELT script and dbt in a separate virtual environment), so no Docker socket is mounted.

## Project Structure

```text
01-custom-elt-project/
├── airflow/
│   ├── Dockerfile              # Airflow image + pg client + dbt (own venv)
│   ├── dags/
│   │   └── elt_pipeline.py    # DAG: elt_copy >> dbt_build
│   └── logs/                   # generated, git-ignored
├── elt_script/
│   ├── Dockerfile              # Image for running the ELT script on its own
│   └── elt_script.py           # pg_dump -> psql full copy
├── postgres_transformations/   # dbt project
│   ├── Dockerfile              # Image for running dbt on its own
│   ├── dbt_project.yml
│   ├── profiles.yml            # Reads connection details from environment variables
│   └── models/
│       ├── sources.yml
│       ├── schema.yml
│       └── film_summary.sql
├── source_db_init/
│   └── init.sql                # Creates and seeds the source database
├── .env.example                # Template for environment variables
├── .gitignore
├── docker-compose.yaml
└── README.md
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose, with at least 4 GB of memory allocated to Docker
- Git

## Getting Started

1. **Clone the repo and move into the project**
   ```bash
   git clone https://github.com/<your-username>/data-engineering-projects.git
   cd data-engineering-projects/01-custom-elt-project
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env`: set the database passwords and the Airflow admin password, and generate the two Airflow secrets:
   ```bash
   docker run --rm apache/airflow:3.3.2 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"   # FERNET_KEY
   docker run --rm apache/airflow:3.3.2 python -c "import secrets; print(secrets.token_urlsafe(32))"                                 # AIRFLOW__API_AUTH__JWT_SECRET
   ```

3. **Create the Airflow folders**
   ```bash
   mkdir -p airflow/dags airflow/logs
   ```

4. **Start the services**
   ```bash
   docker compose up -d --build
   ```
   The first build takes several minutes.

5. **Run the pipeline**
   Open http://localhost:8080 and log in with the Airflow admin username and password from `.env`. Switch on the `elt_pipeline` DAG and click **Trigger**. Both tasks (`elt_copy`, `dbt_build`) should turn green.

6. **Verify the data**
   ```bash
   docker compose exec destination_postgres psql -U postgres -d destination_db -c "\dt"
   docker compose exec destination_postgres psql -U postgres -d destination_db -c "SELECT film_id, title, categories FROM analytics.film_summary ORDER BY film_id LIMIT 5;"
   ```
   Expected: tables `actors`, `film_actors`, `film_category`, `films`, `users`, and 20 rows in `analytics.film_summary`.

7. **Shut down**
   ```bash
   docker compose down        # stop containers
   docker compose down -v     # also remove database volumes
   ```

## Configuration

Settings are read from `.env`; see `.env.example` for the full list.

| Variable | Used for |
|----------|----------|
| `SOURCE_DB_*`, `DEST_DB_*` | Source and destination connections (also used by the ELT script and dbt) |
| `FERNET_KEY`, `AIRFLOW__API_AUTH__JWT_SECRET` | Airflow encryption and API token signing |
| `_AIRFLOW_WWW_USER_USERNAME`, `_AIRFLOW_WWW_USER_PASSWORD` | Airflow admin login |
| `AIRFLOW_UID` | User ID Airflow runs as (leave at 50000) |

> ⚠️ Never commit your real `.env` file. It is excluded via `.gitignore`.

Host ports: Airflow UI `8080`, source database `5433`, destination database `5434`.

## How It Works

1. **Source DB** starts and is seeded from `init.sql`.
2. **`elt_copy`** dumps the source with `pg_dump --clean --if-exists` and loads it into the destination with `psql` (`ON_ERROR_STOP=1`), so it can be re-run safely and fails on any SQL error.
3. **`dbt_build`** reads the copied `public` tables as sources, tests them, and builds `analytics.film_summary`. Models are materialised as **tables**, because the ELT drops and recreates the `public` tables on every run and views depending on them would block that.
4. **Airflow** orders the two tasks, retries a failed task once, keeps logs, and runs the DAG daily.

## Running Steps Without Airflow

The standalone ELT and dbt containers still work, as a fallback or for debugging:
```bash
docker compose run --rm elt_script
docker compose run --rm dbt        # also runs elt_script first
```

## Roadmap

- [x] Project scaffolding and environment configuration
- [x] Source database initialisation (`init.sql`)
- [x] Dockerised, re-runnable ELT script
- [x] dbt models and tests
- [x] Orchestration with Apache Airflow
- [ ] Add architecture diagram and screenshots to `assets/`

[← Back to main README](../README.md)