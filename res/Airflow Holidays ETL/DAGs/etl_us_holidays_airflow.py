from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pendulum
import requests
import json

#Extract_holidays 
def extract_holidays(**context):
    all_holidays = []

    for year in range(2015, 2027):
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/US"
        res = requests.get(url)
        res.raise_for_status()
        holidays = res.json()

        all_holidays.extend(holidays)

    context['ti'].xcom_push(key='raw_holidays', value=all_holidays)

default_args = {
    'start_date': pendulum.datetime(2025, 8, 3, tz="UTC")
}

with DAG(
    dag_id='etl_us_holidays_airflow',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_holidays',
        python_callable=extract_holidays,
    )
#Transform-->NY
    def filter_new_york_holidays(**context):
        raw_holidays = context['ti'].xcom_pull(key='raw_holidays', task_ids='extract_holidays')
        ny_holidays = []

        for holiday in raw_holidays:
            counties = holiday.get("counties")
            if counties and "US-NY" in counties:
                ny_holidays.append(holiday)

        context['ti'].xcom_push(key='ny_holidays', value=ny_holidays)

    filter_task = PythonOperator(
     task_id='filter_ny_holidays',
     python_callable=filter_new_york_holidays,
    )

#Load in MYSQL
    def load_to_mysql(**context):
        ny_holidays = context['ti'].xcom_pull(key='ny_holidays', task_ids='filter_ny_holidays')
        hook = MySqlHook(mysql_conn_id='mysql_default')

        insert_sql = """
            INSERT IGNORE INTO us_holidays_airflow
            (date, local_name, country_code, fixed, global, counties, launch_year, type, day_of_week)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

            """

        conn = hook.get_conn()
        cursor = conn.cursor()

        for h in ny_holidays:
            cursor.execute(insert_sql, (
                h.get('date'),
                h.get('localName'),
                h.get('countryCode'),
                h.get('fixed'),
                h.get('global'),
                json.dumps(h.get('counties')),
                h.get('launchYear', 0),
                h.get('type', 'unknown'),
                pendulum.parse(h.get('date')).format('dddd')
            ))



        conn.commit()
        cursor.close()
        conn.close()

    load_task = PythonOperator(
        task_id='load_to_mysql',
        python_callable=load_to_mysql,
    )
    extract_task >> filter_task >> load_task