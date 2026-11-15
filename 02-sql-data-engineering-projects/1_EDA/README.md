# Exploratory Data Analysis with SQL: Job Market Analysis

![Project 1 Overview](../Images/1_1_Project1_EDA.png)

A SQL project analyzing the data engineer job market using real-world job posting data. It demonstrates my ability to **write production-quality analytical SQL, design efficient queries, and turn business questions into data-driven insights**.

## Executive Summary

- **Project scope:** Built **3 analytical queries** that answer key questions about the data engineer job market
- **Data modeling:** Used **multi-table joins** across fact and dimension tables to extract insights
- **Analytics:** Applied **aggregations, filtering, and sorting** to find top skills by demand, salary, and overall value
- **Outcomes:** Delivered **actionable insights** on SQL/Python dominance, cloud trends, and salary patterns

If you only have a minute, review these:

1. [`01_top_demanded_skills.sql`](./01_top_demanded_skills.sql) - demand analysis with multi-table joins
2. [`02_top_paying_skills.sql`](./02_top_paying_skills.sql) - salary analysis with aggregations
3. [`03_optimal_skills.sql`](./03_optimal_skills.sql) - combined demand/salary optimization query

## Problem & Context

Job market analysts need to answer questions like:

- **Most in-demand:** *Which skills are most in demand for data engineers?*
- **Highest paid:** *Which skills command the highest salaries?*
- **Best trade-off:** *What is the optimal skill set balancing demand and compensation?*

This project analyzes a **data warehouse** built using a star schema design. The warehouse structure consists of:

![Data Warehouse](../Images/1_2_Data_Warehouse.png)

- **Fact table:** `job_postings_fact` - central table containing job posting details (job titles, locations, salaries, dates, etc.)
- **Dimension tables:**
  - `company_dim` - company information linked to job postings
  - `skills_dim` - skills catalog with skill names and types
- **Bridge table:** `skills_job_dim` - resolves the many-to-many relationship between job postings and skills

By querying across these interconnected tables, I extracted insights about skill demand, salary patterns, and optimal skill combinations for data engineering roles.

## Tech Stack

- **Query engine:** DuckDB for fast OLAP-style analytical queries
- **Language:** SQL (ANSI-style with analytical functions)
- **Data model:** Star schema with fact, dimension, and bridge tables
- **Development:** VS Code for SQL editing + terminal for the DuckDB CLI
- **Version control:** Git/GitHub for versioned SQL scripts

## Analysis Overview

1. **[Top Demanded Skills](./01_top_demanded_skills.sql)** - identifies the 10 most in-demand skills for remote data engineer positions
2. **[Top Paying Skills](./02_top_paying_skills.sql)** - analyzes the 25 highest-paying skills with salary and demand metrics
3. **[Optimal Skills](./03_optimal_skills.sql)** - calculates an optimal score using the natural log of demand combined with median salary to identify the most valuable skills to learn

### Example Query

```sql
SELECT
    sd.skills,
    COUNT(jpf.*) AS demand_count
FROM job_postings_fact AS jpf
INNER JOIN skills_job_dim AS sjd
    ON jpf.job_id = sjd.job_id
INNER JOIN skills_dim AS sd
    ON sjd.skill_id = sd.skill_id
WHERE
    jpf.job_title_short = 'Data Engineer'
    AND jpf.job_work_from_home = True
GROUP BY
    sd.skills
ORDER BY
    demand_count DESC
LIMIT 10;
```

### Key Insights

- **Core languages:** SQL and Python each appear in ~29,000 job postings, making them the most demanded skills
- **Cloud platforms:** AWS and Azure are critical for modern data engineering roles
- **Infrastructure & tooling:** Kubernetes, Docker, and Terraform are associated with premium salaries
- **Big data tools:** Apache Spark shows strong demand with competitive compensation

## SQL Skills Demonstrated

### Query Design & Optimization

- **Complex joins:** multi-table `INNER JOIN` operations across `job_postings_fact`, `skills_job_dim`, and `skills_dim`
- **Aggregations:** `COUNT()`, `MEDIAN()`, `ROUND()` for statistical analysis
- **Filtering:** boolean logic with `WHERE` clauses and multiple conditions (`job_title_short`, `job_work_from_home`, `salary_year_avg IS NOT NULL`)
- **Sorting & limiting:** `ORDER BY` with `DESC` and `LIMIT` for top-N analysis

### Data Analysis Techniques

- **Grouping:** `GROUP BY` for categorical analysis by skill
- **Conditional logic:** `CASE WHEN` statements for derived metrics
- **Mathematical functions:** `LN()` for natural logarithm transformation to normalize demand metrics
- **Calculated metrics:** derived optimal score combining log-transformed demand with median salary
- **`HAVING` clause:** filtering aggregated results (skills with >= 100 postings)
- **NULL handling:** filtering out incomplete records (`salary_year_avg IS NOT NULL`)

[← Back to SQL projects](../README.md)