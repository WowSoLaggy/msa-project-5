from datetime import datetime, timedelta
import os
import pandas as pd
import random

from airflow import DAG
from airflow.operators.email  import EmailOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


default_args = {
    "owner": "admin",
    "retries": 2,
    "retry_delay": timedelta(seconds=10),
    "retry_exponential_backoff": True,
    # email “из коробки” при ошибке/ретрае
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": True,
}



def read_csv():
  df = pd.read_csv('/opt/airflow/data/input.csv')
  df.to_pickle('/opt/airflow/data/raw_data.pkl')


def transform_data():
  df = pd.read_pickle('/opt/airflow/data/raw_data.pkl')
  df['bonus_money'] = df['money'] * 2
  df.to_pickle('/opt/airflow/data/processed_data.pkl')


def analyze_with_condition():
  df = pd.read_pickle('/opt/airflow/data/processed_data.pkl')
  print(f"Total bonus money: {df['bonus_money'].sum()}")
  if random.random() > 0.5:
    return 'email_success'
  else:
    return 'email_fail'
  

def finalize():
  print("Pipeline finished.")


with DAG(
    dag_id="task1_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    read_csv_task = PythonOperator(
      task_id="read_csv_job",
      python_callable=read_csv,
    )

    transform_data_task = PythonOperator(
      task_id="transform_data_job",
      python_callable=transform_data,
    )

    analyze_with_condition_task = BranchPythonOperator(
      task_id="analyze_with_condition_job",
      python_callable=analyze_with_condition,
    )

    email_success = EmailOperator(
        task_id="email_success",
        to=["admin@example.com"],
        subject="Airflow success",
        html_content="""
        <p>DAG success</p>
        """,
        trigger_rule="none_failed_min_one_success",
    )

    email_fail = EmailOperator(
        task_id="email_fail",
        to=["admin@example.com"],
        subject="Airflow fail",
        html_content="""
        <p>DAG fail</p>
        """,
        trigger_rule="none_failed_min_one_success",
    )

    finalize_task = PythonOperator(
      task_id="finalize_job",
      python_callable=finalize,
      trigger_rule='none_failed_min_one_success',
    )

    read_csv_task >> transform_data_task >> analyze_with_condition_task
    analyze_with_condition_task >> [ email_success, email_fail ] >> finalize_task
