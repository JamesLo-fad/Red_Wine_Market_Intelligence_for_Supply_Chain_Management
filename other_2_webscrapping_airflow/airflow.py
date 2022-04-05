from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

with DAG(
    'Webscrapping_redwine',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 3, 4),
    catchup=False,
) as dag:

    kubernetes_min_pod = KubernetesPodOperator(
        task_id='Redwine_scrapping',
        name='pod-ex-minimum',
        namespace='default',
        image='gcr.io/divine-builder-342012/airflow_01')
