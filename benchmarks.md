## Docker Stats

results for `docker stats` command

original `apache-airflow/2.6.1/docker-compose.yaml` stats usage (2023-06-10): 
```
CONTAINER ID   NAME                                        CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O   PIDS
5867acefbaa6   spotify-data-pipeline-airflow-webserver-1   0.10%     629.2MiB / 3.837GiB   16.01%    2.24MB / 7.71MB   0B / 0B     9
4e7d6a6f34d5   spotify-data-pipeline-airflow-scheduler-1   1.75%     284.9MiB / 3.837GiB   7.25%     2.58MB / 3.71MB   0B / 0B     4
041b7fb79c03   spotify-data-pipeline-airflow-triggerer-1   0.91%     202.6MiB / 3.837GiB   5.16%     418kB / 615kB     0B / 0B     7
804d2a45a8ff   spotify-data-pipeline-airflow-worker-1      0.09%     1.64GiB / 3.837GiB    42.74%    84.2kB / 99.6kB   0B / 0B     21
343efe54068e   spotify-data-pipeline-redis-1               0.12%     10.77MiB / 3.837GiB   0.27%     79.8kB / 65.6kB   0B / 0B     5
4b98186e4bba   spotify-data-pipeline-postgres-1            0.79%     73.77MiB / 3.837GiB   1.88%     5.7MB / 5.26MB    0B / 0B     22
```

modified (2023-06-10):
- from `postgres:13` to `postgres:13.11-alpine3.18`
- from `redis:latest` to `redis:7.0.11-alpine3.18`

```
CONTAINER ID   NAME                                        CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O   PIDS
cda17031f0a5   spotify-data-pipeline-airflow-triggerer-1   75.80%    277.8MiB / 3.837GiB   7.07%     308kB / 455kB     0B / 0B     9
cb4069fb192d   spotify-data-pipeline-airflow-webserver-1   0.10%     634.6MiB / 3.837GiB   16.15%    1.59MB / 1.15MB   0B / 0B     9
7cad2498f4f4   spotify-data-pipeline-airflow-scheduler-1   2.79%     279.3MiB / 3.837GiB   7.11%     1.74MB / 2.04MB   0B / 0B     4
b76cbe09c6b4   spotify-data-pipeline-airflow-worker-1      54.91%    1.648GiB / 3.837GiB   42.94%    63.2kB / 76.2kB   0B / 0B     21
c10fa403a247   spotify-data-pipeline-postgres-1            3.42%     48.37MiB / 3.837GiB   1.23%     3.82MB / 4.18MB   0B / 0B     22
0bbf571262eb   spotify-data-pipeline-redis-1               0.37%     3.32MiB / 3.837GiB    0.08%     57.8kB / 45.8kB   0B / 0B     5
```