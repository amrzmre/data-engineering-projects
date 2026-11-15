# SQL Data Engineering Projects

A collection of SQL projects I built to practice and reinforce my data engineering skills: querying, dimensional modelling, ETL pipelines, and data mart design.

> Click a project name below to see the tools and techniques I used to build it.

## Projects

### [1. EDA](./1_EDA/) - Exploratory Data Analysis

![Project 1 Overview](./Images/1_1_Project1_EDA.png)

SQL-driven analysis of the data engineer job market, using multi-table joins, aggregations, and calculated metrics to answer which skills are most in demand, best paid, and most worth learning.

**Skills:** Multi-table joins, aggregations, filtering, top-N analysis, calculated metrics

### [2. DW & Mart Build](./2_DW_Mart_Build/) - Data Pipeline: Data Warehouse & Marts

![Data Pipeline Architecture](./Images/1_2_Project2_Data_Pipeline.png)

End-to-end ETL pipeline that transforms raw CSV files into a star schema data warehouse and builds analytical data marts.

**Skills:** Dimensional modelling, ETL pipeline development, data mart architecture, incremental updates (`MERGE`), production practices

## Lessons

Practice scripts from each lesson of the course, covering JOINs, DDL/DML, CTEs, window functions, and more. See the [Lessons index](./Lessons/).

## Repository Structure

```text
02-sql-data-engineering-projects/
├── 1_EDA/                  # Project 1: job market analysis queries
├── 2_DW_Mart_Build/        # Project 2: warehouse + marts pipeline
├── Images/                 # Diagrams used in the READMEs
├── Lessons/                # Lesson-by-lesson practice scripts (1.09 - 1.32)
├── .gitignore
└── README.md
```

## Tech Stack

- **SQL** (DDL, DML, analytical functions, `MERGE`)
- **DuckDB** as the analytical query engine
- **Google Cloud Storage** as the source of the raw CSV files
- **VS Code** + DuckDB CLI for development
- **Git / GitHub** for version control

## Getting Started

1. [Install DuckDB](https://duckdb.org/docs/installation)
2. Build the warehouse and marts by following the steps in [`2_DW_Mart_Build`](./2_DW_Mart_Build/#how-to-run)
3. Run the analysis queries in [`1_EDA`](./1_EDA/)

## Acknowledgements

<!-- TODO: confirm the course name and link are correct -->
Built while following the [SQL Data Engineering Course](https://github.com/lukebarousse/SQL_Data_Engineering_Course) by Luke Barousse. The dataset and some diagrams come from that course.

[← Back to main README](../README.md)

# DuckDB database files
*.duckdb
*.duckdb.wal