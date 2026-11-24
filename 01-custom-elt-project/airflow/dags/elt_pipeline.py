from datetime import datetime, timedelta

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

DBT = "/home/airflow/dbt-venv/bin/dbt"
DBT_DIR = "/opt/airflow/dbt"

with DAG(
    dag_id="elt_pipeline",
    description="Copy source DB to destination DB, then build dbt models",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",  # was: schedule=None  # manual trigger for now; we'll add a schedule after the first successful run
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=1)},
    tags=["elt"],
) as dag:
    elt_copy = BashOperator(
        task_id="elt_copy",
        bash_command="python /opt/airflow/elt_script/elt_script.py",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"{DBT} build --project-dir {DBT_DIR} --profiles-dir {DBT_DIR}",
        # keep dbt's generated files out of the mounted project folder
        env={"DBT_TARGET_PATH": "/tmp/dbt_target", "DBT_LOG_PATH": "/tmp/dbt_logs"},
        append_env=True,
    )

    elt_copy >> dbt_build