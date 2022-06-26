# Glints

### Objective
- Transfer data of a table in a source postgres DB to a target postgres DB using Airflow


### Solution
- Hosted two postgres DB as my source and target
    - Both DB have been initialized with the dummy table - `sql.table.sql`
    ```
    |id|sale_value|created_at|
    ```
    - Source DB is then inserted 3 rows of data - `sql/data.sql`

- Airflow
    - Webserver is setup using a prebuilt image - https://github.com/puckel/docker-airflow and hosted on http://localhost:5884/ as requested
    - A separate postgres DB is initialized to store airflow's metadata


- DAG
    - a dag is created to retrieve data from source, and write data to target - `dags/pipeline.py`
        - it is set to run once only
        - it has two task:
            1. get data from source
            2. write data to target


### Steps on running the entire solution
1. Run `docker-compose up`
2. Access the airflow's webserver at http://localhost:5884/ 
3. Under the `DAG` tab, turn on `DAG_TRANSFER_DATA_FROM_SOURCE_TO_TARGET`
4. After the successfully running the dag, using `DBeaver`, access the target postgres DB
5. Run `SELECT * FROM public.sales_target` and you should see 3 records
6. It should look something like this
![image](images/result.jpg)



### Access
- Source DB
    - Username: admin
    - Password: password
    - Database Name: postgres
    - Database Host: localhost
    - Port: 5432

- Target DB
    - Username: admin
    - Password: password
    - Database Name: postgres
    - Database Host: localhost
    - Port: 5433
