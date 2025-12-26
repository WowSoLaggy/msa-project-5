from datetime import datetime
import os
import pandas as pd
import random

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator


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
    return 'show_me_the_money_job'
  else:
    return 'no_money_job'
  

def show_me_the_money():
  print("Big bonus! Show me the money!")

def no_money():
  print("No big bonus this time.")

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

    show_me_the_money_task = PythonOperator(
      task_id="show_me_the_money_job",
      python_callable=show_me_the_money,
    )

    no_money_task = PythonOperator(
      task_id="no_money_job",
      python_callable=no_money,
    )

    finalize_task = PythonOperator(
      task_id="finalize_job",
      python_callable=finalize,
    )

    read_csv_task >> transform_data_task >> analyze_with_condition_task
    analyze_with_condition_task >> [show_me_the_money_task, no_money_task] >> finalize_task
