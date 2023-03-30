#created by joshua Omolewa

import airflow
from airflow import DAG
from datetime import timedelta
from airflow.operators.python_operator import PythonOperator  #importing operator to use python fucntions
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator #importing  EMR operator to perform submit EMR jobs as steps
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor #importing  EMR sensor  to check status of EMR jobs
import json 



SPARK_STEPS = [
    {
        'Name': 'joshua_data_engineer',
        'ActionOnFailure': "CONTINUE",
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                '/usr/bin/spark-submit',
                '--class', 'Driver.MainApp',
                '--master', 'yarn',
                '--deploy-mode', 'cluster',
                '--num-executors', '2',
                '--driver-memory', '512m',
                '--executor-memory', '3g',
                '--executor-cores', '2',
                '--py-files','s3://project-spark-script-josh/job.zip', 
                's3://spark-workflow/workflow_entry.py',
                '-p', json.dumps({'calendar': "{{ task_instance.xcom_pull('parse_request', key='calendar') }}",
                 'sales': "{{ task_instance.xcom_pull('parse_request', key='sales') }}",
                 'inventory': "{{ task_instance.xcom_pull('parse_request', key='inventory') }}",
                 'product': "{{ task_instance.xcom_pull('parse_request', key='product') }}",
                 'store': "{{ task_instance.xcom_pull('parse_request', key='store') }}",
                 'output_path': "s3://transformed-data-project/weekly-fact-table",'partition_column':'cal_dt',
                 'output_path1': "s3://transformed-data-project/store_dim_table",'partition_column1':'CNTRY_CD',
                 'output_path2': "s3://transformed-data-project/product_dim_table",'partition_column2':'PROD_NAME',
                 'output_path3': "s3://transformed-data-project/calendar_dim_table",'partition_column3':'WEEK_NUM',
                 'name':'project'
                 })
            ]
        }
    }

]

CLUSTER_ID = 'j-2OMRCVNXRKC9N'

DEFAULT_ARGS = {
    'owner': 'joshua_data_engineer',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),   #defining when airflow starts executing the task 
    'email': ['airflow_info@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

def retrieve_s3_files(**kwargs):  
    """
    This function is used to retreive S3 csv file locations sent from lamba json conf payload
    """
    calendar = kwargs['dag_run'].conf['calendar']  #retreiving s3 location for calendar_csv file 
    kwargs['ti'].xcom_push(key = 'calendar', value = calendar)  #creating a key in xcom that can be called by other operators
    store = kwargs['dag_run'].conf['store']  #retreiving s3 location for store_csv file 
    kwargs['ti'].xcom_push(key = 'store', value = store)
    inventory = kwargs['dag_run'].conf['inventory']   #retreiving s3 location for inventory_csv file 
    kwargs['ti'].xcom_push(key = 'inventory', value = inventory)
    product = kwargs['dag_run'].conf['product']    #retreiving s3 location for product_csv file 
    kwargs['ti'].xcom_push(key = 'product', value = product)
    sales = kwargs['dag_run'].conf['sales']   #retreiving s3 location for sales_csv file 
    kwargs['ti'].xcom_push(key = 'sales', value = sales)





dag = DAG(
    'joshua_project_trigger',    #DAG ID
    default_args = DEFAULT_ARGS,
    dagrun_timeout = timedelta(hours=2),
    schedule_interval = None   #defining shedule interval for task, None is situable for manually trigger job via Aireflow REST API
)

#TASKS TO BE EXECUTED BY AIRFLOW

#TASK 1 : parse request
parse_request = PythonOperator(task_id = 'parse_request', 
                                provide_context = True, # Airflow will pass a set of keyword arguments(payload sent from lambda will be accessible) that can be used in your function
                                python_callable = retrieve_s3_files, #calling the function defined
                                dag = dag
                                )


#TASK 2 : Adding step to EMR cluster
step_adder = EmrAddStepsOperator(
    task_id = 'add_steps',
    job_flow_id = CLUSTER_ID,
    aws_conn_id = "aws_default",
    steps = SPARK_STEPS,
    dag = dag
)

#TASK 3: Checking the status of job in EMR cluster
step_checker = EmrStepSensor(
    task_id = 'watch_step',
    job_flow_id = CLUSTER_ID,
    step_id = "{{ task_instance.xcom_pull('add_steps', key='return_value')[0] }}",
    aws_conn_id = "aws_default",
    dag = dag
)


#SETTING THE DEPENDECIES ( This instruct aiflow  on the task depencies)
# step_adder.set_upstream(parse_request)
# step_checker.set_upstream(step_adder)

#OR

parse_request >> step_adder >> step_checker