# Retail Store End-To-End Batch Data-pipeline (ETL) Project

# Author: 👤 **Joshua Omolewa**

## PROJECT OVERVIEW : Building a Data Pipeline for  a Retail store using AWS services that collects  data from its transactional database (OLTP) in Snowflake  and transforms the collected data (ETL process) using spark to meet  business requirements and also enables  Data Analyst/BI professionals to run SQL query & create Data Visualization using Superset

## 1. Project Architecture

![project architecture](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Data%20Architecture.jpg)

## 1. Business Scenario
A Retail Store requires a Data engineer to build a data pipeline (ETL) that take raw data from organization database and transforms the data to satisfy the business buisness  requirements and  provide a platform for Data Analyst to generate Visualization to answer some business questions.

## 2. Business Requirements
The data engineer is require to produce a weekly table that meets the following requirements for Data Analyst can perform analytics:

The table will be grouped by each week, each store, each product to calculate the following metrics: (**I transalated the business requirement to mini SQL statement I will need during transformation process using Spark**)

* total sales quantity of a product : **Sum(sales_qty)**
* total sales amount of a product : **Sum(sales_amt)**
* average sales Price: **Sum(sales_amt)/Sum(sales_qty)**
* stock level by then end of the week : **stock_on_hand_qty by the end of the week (only the stock level at the end day of the week)**
* store on Order level by then end of the week: **ordered_stock_qty by the end of the week (only the ordered stock quantity at the end day of the week)**
* total cost of the week: **Sum(cost_amt)**
* the percentage of Store In-Stock: **(how many times of out_of_stock in a week) / days of a week (7 days)**
* total Low Stock Impact: **sum (out_of+stock_flg + Low_Stock_flg)**
* potential Low Stock Impact: **if Low_Stock_Flg =TRUE then SUM(sales_amt - stock_on_hand_amt)**
* no Stock Impact: **if out_of_stock_flg=true, then sum(sales_amt)**
* low Stock Instances: **Calculate how many times of Low_Stock_Flg in a week**
* no Stock Instances: **Calculate then how many times of out_of_Stock_Flg in a week**
* how many weeks the on hand stock can supply: **(stock_on_hand_qty at the end of the week) / sum(sales_qty)**

## 3. STEPS USED TO COMPLETE THE PROJECT 

* Load the [raw data](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing) into snowflake in order to setup the Snowfalke OLTP system 
<img src="[https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowflake%20load%20data%20into%20database.jpg](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowfalke%20final.jpg)"  width="100%" height="100%">

* Database: The transactional database is Snowflake and the [raw data](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing) is loaded into snowflake tables from S3 bucket (see image below for snowflake table). The data from snowflake is automatically move at 12:00am MST everyday to the staging area using store procedure i.e Input S3 bucket.
* Input S3 bucket: The first S3 bucket is created as a staging area for the raw data coming from the Snowflake. The raw data is extracted from the snowflake database using store procedure and chron job in snowflake which ensures data is moved from OLTP system at 12:00am to the s3 bucket everyday. Sample raw data from in the s3 bucket is shown in the image below. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/raw%20data%20extracted%20to%20s3.jpg"  width="100%" height="100%">
*Programming languages : Python, SQL langauges are used to build the pyspark script that utilizes SparkSQL API for transforming the raw data to meet the business requirement using the Amazon EMR cluster. 
* Lambda : A lambda function is created and  required to send the raw data in the S3 staging area by triggering airflow.The lambda function triggers airflow workflows automatically & the lambda function is automatically triggered at 12:05am MST (this time is used as the raw data come into input s3 bucket by 12:00am MST everyday) by CloudWatch and if the data is not available to be sent an email is sent to notify the data engineer that the data from the transactional database has not been received.<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/lambda%20function%20to%20trigger%20airflow%20and%20send%20email.jpg"  width="100%" height="100%">
* Cloudwatch: Cloudwatch is used to set a rule that automatically triggers the Lambda function at 12:05am . <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/cloudwatch%20rule.jpg"  width="100%" height="100%">
* Aiflow: Airflow runs in a docker container within an EC2 instance  & it   is used to orchestrate & schedule the the movement of data from S3 to the EMR cluster for transformation. Airflow also monitor the spark job transfromation step in the EMRcluster and displays if the step executed successfully in DAG Graph view. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Airflow.jpg"  width="100%" height="100%">
* EMR : The EMR cluster has hadoop & spark installed and will transform the raw data configuration received from airflow using spark streaming to meet the business requirement  and send the transform data in parquet format to the output S3  bucket (ETL process). <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/emr%20runing%20spark%20submit%20job.jpg"  width="100%" height="100%">
* Output S3 bucket: Created an S3 bucket in which the transformed data from EMR Cluster is stored.<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/tranformed%20s3%20bucket.jpg"  width="100%" height="100%">
* Glue: Glue is used  to automatically crawl the output S3 bucket to create tables in the Glue catalog that can be queried using Athena by the data analyst .<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/AWS%20glue%20crawler%20final.jpg"  width="100%" height="100%">
* Athena: Athena is used to Query the tables created using Glue. The Data anlyst can interact with the weekly table using SQL in order to answer business questions. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Anthena%20final.jpg"  width="100%" height="100%">
* Superset: Superset runs in a docker container in an EC2 instance that can be used to create Data Visualization  & dashboards  by the Data Analyst. <img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Superset%20finals.jpg"  width="100%" height="100%">


# 4. STEPS USED TO COMPLETE THIS PROJECT
* Load the [raw data](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing) into snowflake in order to setup the Snowfalke OLTP system 
<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowflake%20load%20data%20into%20database.jpg"  width="100%" height="100%">

* Create a store procedure to move the raw data from OLTP into snowflake in order to setup the Snowfalke OLTP system 
<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowflake%20load%20data%20into%20database.jpg"  width="100%" height="100%">

* SSH into EC2 instance (ensuring my ip is allowed to access instance through the security group) via VSCODE (using remote explorer) and create the project structure containing shell scripts (init.sh, run.sh), python scripts( run.py), .env file(to store access keys to my AWS console), .config.toml file (containing config files to access specific S3 bucket directory and to store API url), .gitignore to ignore specific files (.env and virtual environment folder created by runing init.sh),requirments.txt (containing all library dependencies required for the project)
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/ssh.jpg"  width="100%" height="100%">

* Write the code into the shell scripts (init.sh, run.sh). The init.sh installs required libaries,virtual environment, install the dependencies for the virtual environment from requirment.txt file & create a log folder. I then run the init.sh  using `./init.sh` as shown below to that creates virtual environment folder project_venv and log folder 
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/init.sh.jpg"  width="100%" height="100%">

* Write the code for the python script `run.py` that will be intialized using `run.sh` shell script. The run.sh shell script will also create log files and print out if the python script was successfully executed or not. I run the run.sh script using `./run.sh` , the  python script(run.py) will send request to the API, store the payload, transform the payload to required data partitions based on business requirement, combine data partitions into a single file (job.csv) using pandas library and then job.csv to S3 bucket. The run.sh shell script will create log files each time it is executed and if succesful it print it as shown below
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/project%20complete.jpg"  width="100%" height="100%">

* Checking Amazon S3 bucket to ensure the job.csv file has been successfuly uploaded and viewing a copy in Github repository
<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Superset%20finals.jpg"  width="100%" height="100%">



### Note: (1) Pipeline can be automated using chronjob if needed (2)log folder contains all log files generated when working on the project

## PROJECT FILES

* [init.sh SCRIPT](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/init.sh)

* [run.sh SCRIPT](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/run.sh)

* [run.py SCRIPT](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/run.py)

* [requirements.txt FILE](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/requirements.txt)

* [job.csv DATA FILE](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/job.csv)

* [LOG FOLDER](https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/tree/main/log)

# Follow Me On
  
* LinkedIn: [@omolewajoshua](https://www.linkedin.com/in/joshuaomolewa/)  
* Github: [@joshua-omolewa](https://github.com/Joshua-omolewa)


## Show your support

Give a ⭐️ if this project helped you!
