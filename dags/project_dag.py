# Project ELT Weather - Data extraction from API

# Importing necessary libraries and modules
import datetime as dt  # For handling datetime operations
from datetime import timedelta  # For specifying time intervals
from airflow import DAG  # DAG is the Directed Acyclic Graph used in Airflow to define workflows
from airflow.operators.python_operator import PythonOperator  # Operator to execute Python functions
from datetime import datetime  # For defining the DAG start time
from airflow.utils.dates import days_ago  # Utility to set start date relative to current date
from project_etl import etl_weather  # Importing the custom ETL function from your module

# Default arguments for the DAG
default_args = {
    'owner': 'Shivam V',             # Owner of the DAG
    'depends_on_past': False,             # DAG run does not depend on the success of previous run
    'start_date': dt.datetime.now(),      # Start date of the DAG execution
    'retries': 1,                          # Number of retries in case of failure
    'retry_delay': timedelta(minutes=1)   # Wait time before retrying
}

# Define the DAG
dsa_dag = DAG(
    'project_dag_weather',                # Unique identifier for the DAG
    default_args=default_args,            # Default arguments defined above
    description='Project API Weather',    # Brief description of the DAG
    schedule_interval=timedelta(minutes=60)  # Frequency of execution (every 60 minutes)
)

# Define a task using PythonOperator to execute the ETL function
execute_etl = PythonOperator(
    task_id='project_etl_weather',        # Unique ID for the task
    python_callable=etl_weather,          # Function to be called when task runs
    dag=dsa_dag                           # The DAG to which this task belongs
)

# Set the task to be executed by the scheduler
execute_etl
# This line is necessary to ensure that the task is registered with the DAG