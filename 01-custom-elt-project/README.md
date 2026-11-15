# 01. Custom ELT Project

> 🚧 **Status: In progress.** The ingestion layer is in place; orchestration (Airflow) and transformation (dbt) are planned next.

An end-to-end ELT pipeline demonstrating automated data ingestion, orchestration, and transformation using containerised databases.

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Extract and load script |
| **PostgreSQL** | Source and destination databases |
| **Docker / Docker Compose** | Containerised services |
| **Apache Airflow** | Workflow orchestration *(planned)* |
| **dbt** | SQL-based transformations *(planned)* |

## Architecture

<!-- TODO: add a diagram to /assets and link it here -->
<!-- ![Architecture](../assets/01-elt-architecture.png) -->

```text
Source DB (Postgres)  →  ELT script (Python)  →  Destination DB (Postgres)  →  dbt models
        ▲                                                                          
   init.sql seeds                         Airflow orchestrates the flow (planned)
```

## Project Structure

```text
01-custom-elt-project/
├── elt_script/
│   ├── Dockerfile          # Image for the ELT script container
│   └── elt_script.py       # Extracts from source DB and loads into destination DB
├── source_db_init/
│   └── init.sql            # Creates and seeds the source database on startup
├── .env.example            # Template for environment variables
├── .gitignore
├── docker-compose.yaml     # Defines the databases and ELT service
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
   On first start, `source_db_init/init.sql` creates and seeds the source database, then the ELT script copies the data into the destination database.

4. **Verify the data** *(TODO: adjust names to match your `.env`)*
   ```bash
   docker compose exec <destination-db-service> psql -U <user> -d <database> -c "\dt"
   ```

5. **Shut down**
   ```bash
   docker compose down        # stop containers
   docker compose down -v     # also remove database volumes
   ```

## Configuration

Settings are read from `.env`. See `.env.example` for the full list.

> ⚠️ Never commit your real `.env` file. It is excluded via `.gitignore`.

## How It Works

<!-- TODO: refine to match your implementation -->
1. **Source DB** starts and is initialised with sample data from `init.sql`.
2. **ELT script** (`elt_script.py`) connects to the source, extracts the data, and loads it as-is into the destination database.
3. **Transformation** *(planned)*: dbt models will clean and model the raw data inside the destination database.
4. **Orchestration** *(planned)*: Airflow will schedule and monitor the run.

## Roadmap

- [x] Project scaffolding and environment configuration
- [x] Source database initialisation (`init.sql`)
- [x] Dockerised ELT script
- [x] Docker Compose setup
- [ ] Orchestrate the pipeline with Apache Airflow
- [ ] Add dbt models and tests
- [ ] Add architecture diagram and screenshots to `assets/`

[← Back to main README](../README.md)