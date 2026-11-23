FROM python:3.13-slim

RUN pip install --no-cache-dir "dbt-core~=1.11.0" "dbt-postgres~=1.11.0"

WORKDIR /dbt
ENV DBT_PROFILES_DIR=/dbt
ENTRYPOINT ["dbt"]