# Retail Store End-To-End Batch Data-pipeline (ETL) Project

# Author: 👤 **Joshua Omolewa**

## PROJECT OVERVIEW : I designed and developed a data pipeline for a retail store using AWS services. The pipeline collects data from the store's transactional database (OLTP) in Snowflake and transforms the raw data using Apache Spark to meet the business requirements. The pipeline also enables Data Analysts to run SQL queries and create data visualizations using Superset. The batch ETL pipeline is orchestrated using Airflow, an open-source platform to programmatically author, schedule, and monitor workflows.

##  Project Architecture

![project architecture](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Data%20Architecture.jpg)

## 1. Business Scenario
A Retail Store requires a Data engineer to build a data pipeline (ETL) that extract raw data from the organization database, transforms the data to satisfy buisness  requirements and  provides a platform for Data Analyst to generate visualisations to answer some business questions. The data model for the OLTP database is shown below <img src="https://github.com/Joshua-omolewa/Retailstore_ETL_pipeline_project/blob/main/img/Data%20Model%20for%20Database.jpg"  width="100%" height="100%">



## 2. Business Requirements
The data engineer is required to produce a weekly table that meets the following requirements: This table will enable Data Analyst to answer business questions.

The table will be grouped by each week, each store, each product to calculate the following metrics: (**I translated the business requirement to mini SQL statement I will need during the transformation process using Spark**)

* total quantity of  products : **Sum(sales_qty)**
* total sales amount of products : **Sum(sales_amt)**
* average sales Price: **Sum(sales_amt)/Sum(sales_qty)**
* stock level by then end of the week : **stock_on_hand_qty by the end of the week (only the stock level at the end day of the week)**
* store on Order level by then end of the week: **ordered_stock_qty by the end of the week (only the ordered stock quantity at the end day of the week)**
* total cost for the week: **Sum(cost_amt)**
* the percentage of Store In-Stock: **(how many times of out_of_stock in a week) / days of a week (7 days)**
* total Low Stock Impact: **sum (out_of+stock_flg + Low_Stock_flg)**
* potential Low Stock Impact: **if Low_Stock_Flg =TRUE then SUM(sales_amt - stock_on_hand_amt)**
* no Stock Impact: **if out_of_stock_flg=true, then sum(sales_amt)**
* low Stock Instances: **Calculate how many times of Low_Stock_Flg in a week**
* no Stock Instances: **Calculate then how many times of out_of_Stock_Flg in a week**
* how many weeks the on hand stock can supply: **(stock_on_hand_qty at the end of the week) / sum(sales_qty)**

## 3. STEPS USED TO COMPLETE THE PROJECT 

### Please note: Python language & SQL are used to build the pyspark script that utilizes the SparkSQL API for transforming the raw data to meet the business requirement using the Amazon EMR cluster. 

* I created a database with schema in Snowflake using this   **[SQL DDL script](https://github.com/Joshua-omolewa/Retailstore_ETL_pipeline_project/blob/main/Crerate%20schema%20and%20load%20data%20to%20SNOWFLAKE.sql)**  and then I loaded the **[raw data](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing)** into the Snowflake database in order to setup the Snowflake OLTP system.
<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowfalke%20final.jpg"  width="100%" height="100%">

* I Wrote a SQL [stored procedure](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/snowflake_loading_data_to_s3%20-final.sql) that would initiate the extraction of the raw data into the staging s3 bucket (i.e., input s3 bucket) every day at 12:00 MST, which is the off peak period for the retail store. Snowflakes allows the creation of tasks that utilise chron to run any query. I create a task that runs the store procedure to load the data for each day to the input s3 bucket at  12:00 am MST everyday. This process creates a batch load of raw data at the end of each day to be moved into the staging s3 bucket
  * store procedure sql code
```
--Step 1. Create a procedure to load data from Snowflake table to S3 using SQL format.
CREATE OR REPLACE PROCEDURE COPY_INTO_S3()
-- specifying what data the return value should have
RETURNS DATE
-- Using sql language
LANGUAGE SQL 
AS
$$
BEGIN 
-- First step is to create a dat2 variable that stores  current date function on snowflake  which has YYYY-MM-DD format by default
	LET dat2 STRING := (SELECT CURRENT_DATE());	

--For 1st Table to be loaded to S3 following the step below
-- Next step  is to create a QUERY variable that concatenate the sql query and variable date and then send it  out to S3 bucket for staging based on date in cal_dt column
	LET QUERY0 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/inventory_',:dat2,'.csv FROM (select * from project_db.raw.inventory where cal_dt <= current_date()) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY0);


--For 2nd Table to be loaded to S3 following the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it out to  S3 bucket for staging based on date in trans_dt column
	LET QUERY1 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/sales_',:dat2,'.csv FROM (select * from project_db.raw.sales where trans_dt <= current_date()) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY1);

--For 3rd Table to be loaded to S3 following the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it out to S3 bucket for staging
	LET QUERY2 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/store_',:dat2,'.csv FROM (select * from project_db.raw.store ) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY2);

--For 4th Table to be loaded to S3 following the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it out to S3 bucket for staging
	LET QUERY3 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/product_',:dat2,'.csv FROM (select * from project_db.raw.product ) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY3);

--For 5th Table to be loaded to S3 following the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it  out to S3 bucket for staging
	LET QUERY4 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/calendar_',:dat2,'.csv FROM (select * from project_db.raw.calendar) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY4);

-- RETURNING DATE (OPTIONAL) TO CHECK EVERYTHING IS WORKING
	RETURN dat2;
END;   
$$
;
```
*
  * sql code used to create task and activate task (This task runs the stored procedure)

 ```
  --Step 2. Create a task to run the job. Here we use cron to set job at 12am MST everyday. 
CREATE OR REPLACE TASK load_data_to_s3
WAREHOUSE = PROJECT 
SCHEDULE = 'USING CRON 0 12 * * * America/Edmonton'
AS
CALL COPY_INTO_S3();

--Step 3. Activate the task
ALTER TASK load_data_to_s3 resume;
```

* I created an Input S3 (Amazon Simple Storage Service) bucket as a staging area for the raw data coming from the Snowflake. The raw data is extracted from the snowflake database using store procedure. Sample raw data from in the s3 bucket is shown in the image below. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/raw%20data%20extracted%20to%20s3.jpg"  width="100%" height="100%">


* Utilized  Cloudwatch to pre-set a rule that automatically triggers the Lambda function at 12:05am MST as raw data extracted daily from snowflake  is expected in the s3 staging area by 12:00 a.m. MST . <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/cloudwatch%20rule.jpg"  width="100%" height="100%">

* I created the lambda function that cloudwatch triggers at 12:05 a.m. MST that scans the input s3 bucket (staging area) for yesterday's raw data and if found, the lambda function triggers the airflow workflow automatically to start the batch processing. Also, if the data is not yet available, an email is sent to notify the data engineer that the data from the transactional database has not been received. The python code for the lambda function can be found **[here](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/lambda_function.py)** while the email python code for the lambda function can be found **[here](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/send_email.py)** . Please note that Amazon SES is needed to setup the email notification <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/lambda%20function%20to%20trigger%20airflow%20and%20send%20email.jpg"  width="100%" height="100%"> 

* I created docker containers running Airflow using docker compost  within an EC2 (Amazon Elastic Compute Cloud) instance. Ariflow is used to orchestrate & schedule the the movement of data from S3 to the Amazon EMR cluster for transformation. Airflow submits the spark job to the EMR cluster, and also monitor the spark job transformation step in the EMR cluster and displays if the EMR steps were executed successfully in the DAG Graph view. The airflow python code for the airflow dags can be found **[here](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/airflow_dag.py)**  <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Airflow.jpg"  width="100%" height="100%">

* I created an Amazon EMR cluster that has hadoop & spark frameworks pre-installed. The EMR will transform the raw data to meet the business requirement using pyspark code & spark submit configuration received from airflow and load the transformed data in parquet format to the output S3  bucket (ETL process). The pyspark scripts for the project can be found  **[here](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/tree/main/spark_files)**  <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/emr%20runing%20spark%20submit%20job.jpg"  width="100%" height="100%">

* I created an output S3 bucket in which the transformed data from the EMR Cluster is stored.<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/tranformed%20s3%20bucket.jpg"  width="100%" height="100%">

* Utilised Glue to automatically crawl the output S3 bucket to create tables in the Glue catalogue/database that can be queried using Athena by the data analyst .<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/AWS%20glue%20crawler%20final.jpg"  width="100%" height="100%">

* Made use of Athena to query the tables created using Glue. The Data anlyst can interact with the weekly fact table using SQL in order to answer business questions. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Anthena%20final.jpg"  width="100%" height="100%">


* Finally, I created a docker container that runs superset in an EC2 instance. Superset can be used to create data visualisations  & dashboards  by the Data Analyst. Superset extracts data from Anthena tables, which enables  the Data Analyst to answer any business question. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Superset%20finals.jpg"  width="100%" height="100%">

# Follow Me On
  
* LinkedIn: [@omolewajoshua](https://www.linkedin.com/in/joshuaomolewa/)  
* Github: [@joshua-omolewa](https://github.com/Joshua-omolewa)


## Show your support

Give a ⭐️ if this project helped you!
