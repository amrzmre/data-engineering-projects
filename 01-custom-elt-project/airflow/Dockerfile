FROM apache/airflow:3.3.2

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# Same pg client setup as elt_script/Dockerfile (codename read from the OS)
RUN . /etc/os-release \
    && install -d /usr/share/postgresql-common/pgdg \
    && curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc \
       https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    && echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] http://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main" \
       > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client-18 \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# dbt lives in its own virtual environment so its packages can't clash with Airflow's.
# PIP_USER=false: the Airflow image may default pip to --user mode, which venvs reject.
RUN python -m venv /home/airflow/dbt-venv \
    && PIP_USER=false /home/airflow/dbt-venv/bin/pip install --no-cache-dir \
       "dbt-core~=1.11.0" "dbt-postgres~=1.11.0"