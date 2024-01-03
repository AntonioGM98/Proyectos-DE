from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.sftp.sensors.sftp import SFTPSensor
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.utils.task_group import TaskGroup

import os
from datetime import datetime, timedelta

def decide_branch(**kwargs):
    date = kwargs['execution_date']
    day = date.strftime('%A')
    #print( 'DIA: ', day)
    if day in ['Saturday', 'Sunday']:
        return 'end'
    else:
        return 'weekday'

def create_file(**kwargs):
    sftp_hook = SFTPHook(ftp_conn_id='sftp_connector')
    sftp_client = sftp_hook.get_conn()

    remote_path = '/uploads/practica1_ardillas_{}.csv'.format(kwargs['prev_ds'])

    if not sftp_hook.isfile(remote_path):
        sftp_client.open(remote_path, 'w').close()


def search_next_saturday(execution):
    # 0 = Lunes / 1 = Martes / 2 = Miercoles / ... / 5 = Sabado / 6 = Domingo
    while execution.weekday() != 5:
        execution += timedelta(days=1)
    
    return execution.strftime('%d/%m/%Y')

def process_file(**kwargs):
    sftp_hook = SFTPHook(ftp_conn_id='sftp_connector')
    sftp_client = sftp_hook.get_conn()

    remote_path = '/uploads/practica1{}.csv'.format(kwargs['prev_ds'])

    execution = kwargs['execution_date'].strftime('%d%b%y')

    member = 'Antonio Luis Garcia Moreno'

    next_saturday = search_next_saturday(kwargs['execution_date'])

    content = f"{execution}" \
              f"{member}" \
              f"{next_saturday}"

    new_remote_path = f"/uploads/practica1_ardillas_{kwargs['prev_ds']}_{kwargs['execution_date'].strftime('%A')}.csv"

    with sftp_client.open(new_remote_path, "w") as f:
        f.write(content)

with DAG(dag_id='practica_dag', start_date=datetime(2023,1,1,12,15),
 schedule_interval='15 12 * * *', catchup=False) as dag:

    start = DummyOperator(
        task_id = 'start'
    )

    end = DummyOperator(
        task_id = 'end'
    )

    weekday = DummyOperator(
        task_id = 'weekday'
    )
    
    branch_weekend = BranchPythonOperator(
        task_id = 'branch_weekend',
        python_callable = decide_branch,
        provide_context = True
    )
    
    with TaskGroup('create_and_process') as create_process_task:
        create_file = PythonOperator(
            task_id = 'create_file',
            python_callable = create_file,
            provide_context = True
        )
        

        wait_for_sftp_file = SFTPSensor(
            task_id = 'wait_for_sftp_file',
            sftp_conn_id = 'sftp_connector',
            path = '/uploads/practica1_{{prev_ds}}.csv',
            poke_interval=60,
            mode='reschedule'
        )
        
        write_file = PythonOperator (
            task_id = 'write_file',
            python_callable=process_file,
            provide_context = True
        )

    start >> branch_weekend
    
    branch_weekend >> [weekday, end]
    
    weekday >> create_file >> wait_for_sftp_file  >> write_file >> end