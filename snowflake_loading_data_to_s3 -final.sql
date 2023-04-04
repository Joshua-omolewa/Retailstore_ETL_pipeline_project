

--Step 1. Create a procedure to load data from Snowflake table to S3 using SQL format. Here, replace <your s3 stage name> with your stage name.
CREATE OR REPLACE PROCEDURE COPY_INTO_S3()
-- specifying what data the return value should have
RETURNS DATE
-- Using sql lanaguage
LANGUAGE SQL 
AS
$$
BEGIN 
-- First step is to create a dat2 varaible that stores  current date function on snowflake in which has YYYY-MM-DD format by default
	LET dat2 STRING := (SELECT CURRENT_DATE());	

--For STEP 0 Table to be loaded to S3 with follow the step below
-- Next step  is to create a QUERY variable that concatenate the sql query and variable date and then send it to out S3 bucket for staging based on date in cal_dt column
	LET QUERY0 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/inventory_',:dat2,'.csv FROM (select * from project_db.raw.inventory where cal_dt <= current_date()) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY0);


--For 2nd Table to be loaded to S3 with follow the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it to out S3 bucket for stagingbased on date in trans_dt column
	LET QUERY1 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/sales_',:dat2,'.csv FROM (select * from project_db.raw.sales where trans_dt <= current_date()) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY1);

--For 3rd Table to be loaded to S3 with follow the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it to out S3 bucket for staging
	LET QUERY2 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/store_',:dat2,'.csv FROM (select * from project_db.raw.store ) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY2);

--For 4th Table to be loaded to S3 with follow the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it to out S3 bucket for staging
	LET QUERY3 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/product_',:dat2,'.csv FROM (select * from project_db.raw.product ) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY3);

--For 5th Table to be loaded to S3 with follow the step below
-- Next step is to create a QUERY variable that concatenate the sql query and variable date and then send it to out S3 bucket for staging
	LET QUERY4 STRING := (SELECT CONCAT('COPY INTO @raw_data_stage/calendar_',:dat2,'.csv FROM (select * from project_db.raw.calendar) file_format=(FORMAT_NAME=CSV_COMMA, TYPE=CSV, COMPRESSION=\'NONE\') SINGLE=TRUE HEADER=TRUE MAX_FILE_SIZE=107772160 OVERWRITE=TRUE'));
--  NEXT STEP IS TO EXECUTE our query string above using EXECUTE IMMEDDIATE  below to start the staging process	
	EXECUTE IMMEDIATE (:QUERY4);

-- RETURNING DATE (OPTIONAL) TO CHECK EVERYTHIN IS WORKING
	RETURN dat2;
END;   
$$
;

--Step 2. Create a task to run the job. Here we use cron to set job at 12am MST everyday. 
CREATE OR REPLACE TASK load_data_to_s3
WAREHOUSE = PROJECT 
SCHEDULE = 'USING CRON 0 12 * * * America/Edmonton'
AS
CALL COPY_INTO_S3();


--Step 3. Activate the task
ALTER TASK load_data_to_s3 resume;

--Step 4. Check if the task state is 'started'
USE DATABASE PROJECT_DB;
USE SCHEMA RAW;

DESCRIBE TASK load_data_to_s3;


-- TO SHOW ALL TASK IN DATABASE
SHOW TASKS IN DATABASE PROJECT_DB;