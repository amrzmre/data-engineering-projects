# 01. Custom ELT Project

> 🚧 **Status: In progress.** Ingestion and transformation (dbt) are in place; orchestration (Airflow) is planned next.

An end-to-end ELT pipeline demonstrating automated data ingestion and transformation using containerised databases.

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Extract and load script |
| **PostgreSQL 18** | Source and destination databases |
| **Docker / Docker Compose** | Containerised services |
| **dbt (dbt-core 1.11 + dbt-postgres 1.11)** | SQL-based transformations and tests |
| **Apache Airflow** | Workflow orchestration *(planned)* |

## Architecture

<!-- TODO: add a diagram to /assets and link it here -->
<!-- ![Architecture](../assets/01-elt-architecture.png) -->

```text
Source DB (Postgres)  →  ELT script (Python)  →  Destination DB (Postgres)  →  dbt models
        ▲                  pg_dump → psql          schema: public (raw copy)    schema: analytics
   init.sql seeds

                  Airflow orchestrates the flow (planned)
```

## Project Structure

```text
01-custom-elt-project/
├── elt_script/
│   ├── Dockerfile              # Image for the ELT script container
│   └── elt_script.py           # Extracts from source DB and loads into destination DB
├── postgres_transformations/   # dbt project
│   ├── Dockerfile              # Image with dbt-core and dbt-postgres
│   ├── dbt_project.yml
│   ├── profiles.yml            # Reads connection details from environment variables
│   └── models/
│       ├── sources.yml         # Declares the copied tables + tests
│       ├── schema.yml          # Model tests
│       └── film_summary.sql    # Films with their categories and actors
├── source_db_init/
│   └── init.sql                # Creates and seeds the source database on startup
├── .env.example                # Template for environment variables
├── .gitignore
├── docker-compose.yaml         # Defines the databases, ELT service and dbt service
└── README.md
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
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
   Then edit `.env` with your own values (database names, users, passwords).

3. **Start the services**
   ```bash
   docker compose up --build
   ```
   The services start in this order:
   1. Source and destination databases start; the source is seeded from `source_db_init/init.sql`.
   2. Once both pass their healthchecks, the ELT script copies source → destination and exits.
   3. When the ELT script exits successfully, dbt builds its models and runs its tests, then exits.

4. **Verify the data**

   The commands below assume the default names from `.env.example`; adjust them if you changed `.env`.

   Copied tables (expect `actors`, `film_actors`, `film_category`, `films`, `users`):
   ```bash
   docker compose exec destination_postgres psql -U postgres -d destination_db -c "\dt"
   ```
   dbt output (expect 20 rows):
   ```bash
   docker compose exec destination_postgres psql -U postgres -d destination_db -c "SELECT film_id, title, categories FROM analytics.film_summary ORDER BY film_id LIMIT 5;"
   ```

5. **Shut down**
   ```bash
   docker compose down        # stop containers
   docker compose down -v     # also remove database volumes
   ```

## Configuration

Settings are read from `.env`. See `.env.example` for the full list:

| Variable | Used for |
|----------|----------|
| `SOURCE_DB_NAME`, `SOURCE_DB_USER`, `SOURCE_DB_PASSWORD`, `SOURCE_DB_HOST` | Source database |
| `DEST_DB_NAME`, `DEST_DB_USER`, `DEST_DB_PASSWORD`, `DEST_DB_HOST` | Destination database (also used by dbt) |

> ⚠️ Never commit your real `.env` file. It is excluded via `.gitignore`.

Host ports: source database on `5433`, destination database on `5434`.

## How It Works

1. **Source DB** starts and is initialised with sample data from `init.sql`.
2. **ELT script** (`elt_script.py`) waits for both databases, dumps the source with `pg_dump`, and loads the dump into the destination with `psql`.
   - The dump uses `--clean --if-exists`, so the script can be re-run safely.
   - `psql` runs with `ON_ERROR_STOP=1`, so any failing SQL statement fails the run.
3. **Transformation (dbt):** reads the copied tables in the `public` schema as sources, runs tests on them, and builds `analytics.film_summary`.
   - Models are materialised as **tables**, not views. The ELT drops and recreates the `public` tables on every run, and views depending on them would block that.
4. **Orchestration** *(planned)*: Airflow will schedule and monitor the run.

## Running Individual Steps

Re-run only dbt (the databases must be up and already loaded):
```bash
docker compose up -d source_postgres destination_postgres
docker compose run --rm --no-deps dbt
```

Re-run the full chain (ELT, then dbt):
```bash
docker compose up --build
```

## Roadmap

- [x] Project scaffolding and environment configuration
- [x] Source database initialisation (`init.sql`)
- [x] Dockerised ELT script (re-runnable, with healthcheck-based startup)
- [x] Docker Compose setup
- [x] Add dbt models and tests
- [ ] Orchestrate the pipeline with Apache Airflow
- [ ] Add architecture diagram and screenshots to `assets/`

[← Back to main README](../README.md)