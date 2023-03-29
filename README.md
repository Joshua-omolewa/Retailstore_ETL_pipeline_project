# Retail Store End-To-End Data-pipeline (ETL) Project

# Author: 👤 **Joshua Omolewa**

## PROJECT OVERVIEW : Building a Data Pipeline using AWS services that collects  data from transactional database (OLTP) on Snowflake  and transforms the collected data (ETL process) using spark to meet  business requirements and enables  Data Analyst to run SQL query & create Data Visualization using superset

## 1. Project Architecture

![project architecture](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Data%20Architecture.jpg)

## 1. Business Scenario
A Retail Store requires a Data engineer to build a data pipeline (ETL) that take raw data from organization database and transforms the data to satisfy the business buisness  requirements and  provide a platform for Data Analyst to generate Visualization to answer some business questions.

## 2. Business Requirements
The data engineer is require to produce a weekly table that meets the following requirements:

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

## 3. PRE-REQUISITE
In order to build the architecture the following are required:

* Programming languages : Python, SQL. These langauges are used to build the pyspark script that utilizes SparkSQL API for transforming the raw data to meet the business requirement using the Amazon EMR cluster. 
* Database: The transactional database is Snowflake and the [raw data](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing) is loaded into snowflake from S3 bucket to start this project and also to simulate a real transactional database. The data from snowflake is automatically move at 12:00am MST everyday to the staging area i.e Input S3 bucket. To see how the data was loaded into Snowflake database [click here](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing). To see how the data was automatically move to the s3 bucket at 12:00am MST using store procedure  [click here](https://drive.google.com/drive/folders/1TL3mtDTW4Uv59cyp3C9COgVgGMaBEImB?usp=sharing).
<img src="https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/snowflake%20oltp%20datbase.jpg"  width="100%" height="100%">
* Input S3 bucket: The first S3 bucket is created as a staging area for the raw data coming from the Snowflake.
* Lambda : A lambda function is required to send the raw data in the S3 staging area to airflow.The lambda function triggers airflow workflows automatically & the lambda function is automatically triggered at 12:05am MST by CloudWatch and if the data is not available to be sent an email is sent to notify the data engineer that the data from the transactional database has not been received.
* Cloudwatch: Cloudwatch is used to set a rule that automatically triggers the Lambda function at 12:05am
* Aiflow: Airflow runs in a docker container within an EC2 instance  & it   is used to orchestrate & schedule the the movement of data from S3 to the EMR cluster for transformation. Airflow also monitor the transfromation step in the EMRcluster and displays if the step executed successfully in DAG Tree view.
* EMR : The EMR cluster has hadoop & spark installed and will transform the raw data received from airflow to meet the business requirement  and send the transform data in parquet format to the output S3  bucket (ETL process). 
* Output S3 bucket: The transformed data from EMR Cluster is stored in the Output S3 bucket.
* Glue: Glue is used  to automatically crawl the output S3 bucket to create tables in the Glue catalog that can be queried using Athena by the data analyst
* Athena: Athena is used to Query the tables created using Glue. The Data anlyst can interact with the weekly table using SQL in order to answer business questions
* Superset: Superset runs in a docker container in an EC2 instance that can be used to create Data Visualization  & dashboards  by the Data Analyst


# 4. STEPS USED TO COMPLETE THIS PROJECT
* Create Amazon AWS account and login into AWS console, create Amazon Elastic Compute Cloud (EC2) instance (Ubuntu) and S3 bucket with directory to store transformed csv file. Ensuring EC2 instance and S3 are in created in the same region. Ensure EC2 is attached to default amazon VPC and default subnet so EC2 can have access to internet through default Internet gateway
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/final%20EC2%20S3.jpg"  width="100%" height="100%">

* SSH into EC2 instance (ensuring my ip is allowed to access instance through the security group) via VSCODE (using remote explorer) and create the project structure containing shell scripts (init.sh, run.sh), python scripts( run.py), .env file(to store access keys to my AWS console), .config.toml file (containing config files to access specific S3 bucket directory and to store API url), .gitignore to ignore specific files (.env and virtual environment folder created by runing init.sh),requirments.txt (containing all library dependencies required for the project)
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/ssh.jpg"  width="100%" height="100%">

* Write the code into the shell scripts (init.sh, run.sh). The init.sh installs required libaries,virtual environment, install the dependencies for the virtual environment from requirment.txt file & create a log folder. I then run the init.sh  using `./init.sh` as shown below to that creates virtual environment folder project_venv and log folder 
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/init.sh.jpg"  width="100%" height="100%">

* Write the code for the python script `run.py` that will be intialized using `run.sh` shell script. The run.sh shell script will also create log files and print out if the python script was successfully executed or not. I run the run.sh script using `./run.sh` , the  python script(run.py) will send request to the API, store the payload, transform the payload to required data partitions based on business requirement, combine data partitions into a single file (job.csv) using pandas library and then job.csv to S3 bucket. The run.sh shell script will create log files each time it is executed and if succesful it print it as shown below
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/project%20complete.jpg"  width="100%" height="100%">

* Checking Amazon S3 bucket to ensure the job.csv file has been successfuly uploaded and viewing a copy in Github repository
<img src="https://github.com/Joshua-omolewa/AWS_API_csvdata_to_S3_project/blob/main/img/s3%20succesful%20upload.jpg"  width="100%" height="100%">



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
