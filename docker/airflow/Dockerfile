FROM apache/airflow:slim-2.6.1-python3.10

RUN pip install psycopg2-binary

COPY dags /opt/airflow/dags
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]