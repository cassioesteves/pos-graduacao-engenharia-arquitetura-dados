from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Defina o nome do DAG e seus argumentos padrão
default_args = {
    'owner': 'seu_nome',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Crie um objeto DAG
dag = DAG(
    '0_XPE_exemplo_dag',
    default_args=default_args,
    description='Um exemplo de DAG no Apache Airflow',
    schedule_interval=timedelta(days=1),  # Execução diária
    catchup=False,  # Ignora a execução de datas passadas
)

# Defina tarefas
inicio_tarefa = DummyOperator(
    task_id='inicio_tarefa',
    dag=dag,
)

def imprimir_ola_mundo():
    print("Olá, Mundo!")

tarefa_ola_mundo = PythonOperator(
    task_id='tarefa_ola_mundo',
    python_callable=imprimir_ola_mundo,
    dag=dag,
)

def imprimir_tarefa_concluida():
    print("Tarefa Concluída!")

tarefa_concluida = PythonOperator(
    task_id='tarefa_concluida',
    python_callable=imprimir_tarefa_concluida,
    dag=dag,
)

# Defina a ordem das tarefas
inicio_tarefa >> tarefa_ola_mundo >> tarefa_concluida