from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 24),
    "max_active_runs": 1,
    "retries": 3,
    "retry_delay": timedelta(minutes=60),
    "retry_exponential_backoff": True,
}


def retrieve_data_from_source(**kwargs):
    """
    Create connection with source database, retrieve the data and push it to xcom
    """
    source_db = create_engine(
        "postgresql+psycopg2://admin:password@source_db:5432/postgres"
    )
    conn = source_db.connect()
    query = """SELECT * FROM public.sales_target"""
    result = conn.execute(query).fetchall()
    conn.close()
    kwargs["ti"].xcom_push(key="source_data", value=result)
    return result


def write_data_to_target(**kwargs):
    """
    Create connection with target database, retrieve data from xcom, write it to target
    """
    target_db = create_engine(
        "postgresql+psycopg2://admin:password@target_db:5432/postgres"
    )
    conn = target_db.connect()
    source_data = kwargs["ti"].xcom_pull(key="source_data")

    for datum in source_data:
        query = """INSERT INTO public.sales_target (id, sale_value, created_at)
                    VALUES ({}, {}, '{}')""".format(
            *datum
        )
        conn.execute(query)


# currently set it to run once only
dag = DAG(
    dag_id="DAG_TRANSFER_DATA_FROM_SOURCE_TO_TARGET",
    default_args=args,
    schedule_interval="@once",
)


retrieve_data_from_source_task = PythonOperator(
    task_id="retrieve_data_from_source",
    python_callable=retrieve_data_from_source,
    provide_context=True,
    dag=dag,
)


write_data_to_target_task = PythonOperator(
    task_id="write_data_to_target",
    python_callable=write_data_to_target,
    provide_context=True,
    dag=dag,
)

retrieve_data_from_source_task >> write_data_to_target_task
