from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    '0_XPE_hop_airflow_integration',
    default_args=default_args,
    description='A simple DAG to integrate Apache Hop with Apache Airflow',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['example'],
)

# Set environment variables
hop_env_vars = {
    'HOP_RUN_PARAMETERS': 'INPUT_DIR=/path/to/input/dir',
    'HOP_LOG_LEVEL': 'Basic',
    'HOP_FILE_PATH': '${PROJECT_HOME}/transforms/null-if-basic.hpl',
    'HOP_PROJECT_DIRECTORY': '/project',
    'HOP_PROJECT_NAME': 'TP_ETL',
    'HOP_ENVIRONMENT_NAME': 'env-hop-airflow-sample.json',
    'HOP_ENVIRONMENT_CONFIG_FILE_NAME_PATHS': '/project-config/env-hop-airflow-sample.json',
    'HOP_RUN_CONFIG': 'local',
}

# Bash command to run Hop
bash_command = """
export HOP_RUN_PARAMETERS={{ params.HOP_RUN_PARAMETERS }}
export HOP_LOG_LEVEL={{ params.HOP_LOG_LEVEL }}
export HOP_FILE_PATH={{ params.HOP_FILE_PATH }}
export HOP_PROJECT_DIRECTORY={{ params.HOP_PROJECT_DIRECTORY }}
export HOP_PROJECT_NAME={{ params.HOP_PROJECT_NAME }}
export HOP_ENVIRONMENT_NAME={{ params.HOP_ENVIRONMENT_NAME }}
export HOP_ENVIRONMENT_CONFIG_FILE_NAME_PATHS={{ params.HOP_ENVIRONMENT_CONFIG_FILE_NAME_PATHS }}
export HOP_RUN_CONFIG={{ params.HOP_RUN_CONFIG }}
/path/to/hop/run.sh -r $HOP_RUN_CONFIG -p $HOP_RUN_PARAMETERS
"""

run_hop_task = BashOperator(
    task_id='run_hop',
    bash_command=bash_command,
    params=hop_env_vars,
    dag=dag,
)

run_hop_task