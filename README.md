# Retail Store End-To-End Data-pipeline Project

# Author: 👤 **Joshua Omolewa**

# PROJECT OVERVIEW : Building a Data Pipeline that collects  data from transactional database (OLTP) on Snowflakes  and transforms the collected data to meet  business requirements and enables  Data Analyst to run SQL query & create Data Visualization

## 1. Project Architecture

![project architecture](https://github.com/Joshua-omolewa/end-2-end_data_pipeline_project/blob/main/img/Data%20Architecture.jpg)

## 1. Business Scenario
A Retail Store requires a Data engineer to build a data pipeline that take raw data from organization database and transforms the data to satisfy business buisness  requirements and  provide a platform for Data Analyst to generate Visualization to answer some business questions.

## 2. Business Requirements
The data engineer is require to produce a weekly table that meets the following requirements:

The table will be grouped by each week, each store, each product to calculate the following metrics:

* total sales quantity of a product : Sum(sales_qty)
* total sales amount of a product : Sum(sales_amt)
* average sales Price: Sum(sales_amt)/Sum(sales_qty)
* stock level by then end of the week : stock_on_hand_qty by the end of the week (only the stock level at the end day of the week)
* store on Order level by then end of the week: ordered_stock_qty by the end of the week (only the ordered stock quantity at the end day of the week)
* total cost of the week: Sum(cost_amt)
* the percentage of Store In-Stock: (how many times of out_of_stock in a week) / days of a week (7 days)
* total Low Stock Impact: sum (out_of+stock_flg + Low_Stock_flg)
* potential Low Stock Impact: if Low_Stock_Flg =TRUE then SUM(sales_amt - stock_on_hand_amt)
* no Stock Impact: if out_of_stock_flg=true, then sum(sales_amt)
* low Stock Instances: Calculate how many times of Low_Stock_Flg in a week
* no Stock Instances: Calculate then how many times of out_of_Stock_Flg in a week
* how many weeks the on hand stock can supply: (stock_on_hand_qty at the end of the week) / sum(sales_qty) 

## 3. Deliverable
shell scripts, python script and job.csv to S3.

Shell script: The shell script will control every operation, setting virtual environment, log setting, python script running.

Python script: The Python script is used to transform the data and upload data to s3 bucket.

job.csv: The final transformed data file based on business requirement.

## 4. Specification Detail
The data required is gotten from API by querying jobs from the first 50 pages  https://www.themuse.com/api/public/jobs?page=50




## 6. Project Diagram
 The diagram shows the folder structure for the project and the how the shell scripts create virtual enviroment containing dependecies contained in the requirements.txt file. The run.sh shell script activates the virtual enviroment and run the run.py python script which connect to the API, transform the dat using pandas and then upload the transform job.csv file to S3 bucket for the data analyst
 
![project image](https://github.com/Joshua-omolewa/Scraping_API_csvdata_to_S3_project/blob/main/img/Python_project.png)

# 7. STEPS USED TO COMPLETE THIS PROJECT
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
