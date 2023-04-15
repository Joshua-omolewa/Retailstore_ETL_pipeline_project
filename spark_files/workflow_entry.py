#!/usr/bin/env python3
#AUTHOR: JOSHUA OMOLEWA

import argparse # for argument parsing
import ast
from pyspark.sql import *
from functions import *
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DateType, DoubleType, BooleanType, TimestampType
from pyspark.sql.functions import current_timestamp, max


#using argument parser to parse the argument configurations received from airflow
parser = argparse.ArgumentParser() # get an object from package "argparse" i.e instantiating the argument parser
parser.add_argument("-p", "--params", required=True, help="Spark input parameters") # parse the command line, get the argument after "-p" or "--params"
args = parser.parse_args()  # generate the argument as an object

print('args ' + str(args)) # print out the argument


def parse_command_line(args):
    """
    This function literally evaluate/converts the object srting 
    passed into it and return python native object type i.e dict, bool,int, string i.e Convert a command line argument to a dict
    """
    return ast.literal_eval(args) 


def spark_init(parser_name): # create a spark session
    """
    To initiallize sparkSession
    """
    ss = SparkSession \
        .builder \
        .appName(parser_name)  \
        .getOrCreate()
    ss.sparkContext.setLogLevel("ERROR") # set a logger to show only error messages and not INFO messages when runing spark code
    return ss

params = parse_command_line(args.params) #passing the argument object stored in -p or params to get the dictionary object
print('runnung stuff ' + str(params))

spark = spark_init(params['name']) # create a spark session and storing it in a variable spark




if __name__ == "__main__":


    print("starting spark")

    #STEP 1 READ ALL FILES

    print("reading files")
    
    #reading all csv files and infering their schema
    store_raw_df = read_files( spark, params, store_schema, 'store') #
    # store_raw_df.show()
    # store_raw_df.printSchema()

    calendar_raw_df = read_files( spark, params, calendar_schema, 'calendar') #
    # calendar_raw_df.show()
    # calendar_raw_df.printSchema()

    product_raw_df = read_files( spark, params, product_schema, 'product') #
    # product_raw_df.show()
    # product_raw_df.printSchema()

    inventory_raw_df = read_files( spark, params, invetory_schema, 'inventory') #
    # inventory_raw_df.show()
    # inventory_raw_df.printSchema()

    sales_raw_df = read_files( spark, params, sales_schema, 'sales') #
    # sales_raw_df.show()
    # sales_raw_df.printSchema()


    #STEP 2 CREATING DIMENSION AND FACT TABLES 


    #STORE DIMENSION DATAFRAME
    store_dim_df = store_raw_df.withColumnRenamed('PROV_STATE_DESC','PROV_NAME'). \
        withColumnRenamed('PROV_STATE_CD','PROV_CODE'). \
        drop('FRNCHS_FLGS'). \
        drop('STORE_SIZE')
    # store_dim_df.show()

    #PRODUCT DIMESION DATAFRAME
    product_dim_df = product_raw_df

    #CALENDAR DIMESION DATAFRAME
    calendar_dim_df1 = calendar_raw_df.withColumnRenamed('YR_NUM', 'YEAR_NUM'). \
        withColumnRenamed('WK_NUM', 'WEEK_NUM'). \
        withColumnRenamed('MNTH_NUM', 'MONTH_NUM'). \
        withColumnRenamed('YR_WK_NUM', 'YEAR_WK_NUM'). \
        withColumnRenamed('YR_MNTH_NUM', 'YEAR_MONTH_NUM'). \
        drop('DAY_OF_WK_DESC')

    calendar_dim_df1.show()
    calendar_dim_df = calendar_dim_df1
        
    print("Creating dimension table views for sql query")
    ##### creating temporary view tables for using sql query ######

        #creating views for dimension tables

    sql_table(product_dim_df, 'product_dim')
    sql_table(store_dim_df, 'store_dim')
    sql_table(calendar_dim_df, 'calendar_dim')


    #creating views for raw data
    sql_table(calendar_raw_df, 'calendar')
    sql_table(sales_raw_df, 'sales')
    sql_table(inventory_raw_df, 'inventory')
    sql_table(product_raw_df, 'product')
    sql_table(store_raw_df, 'store')


    print("Generating FACT TABLES Dataframe")
    #DAILY SALES FACT STAGING TABLE
    daily_sale_stg = spark.sql(daily_sale_stg_query) 

    daily_sale_stg.show()
    daily_sale_stg.printSchema()

    #DAILY INVENTORY FACT STAGING TABLE
    daily_inventory_stg = spark.sql(daily_inventory_query) 

    daily_inventory_stg.show() 

    daily_inventory_stg.printSchema() 

   #creating views for fact staging tables
    sql_table( daily_sale_stg, 'daily_sale_stg_df')
    sql_table(daily_inventory_stg, 'daily_inventory_stg_df')

    
    #FINAL DAILY STAGING TABLE
    daily_inventory_stg2 = spark.sql(daily_inventory_query1) #DAILY INVENTORY STAGING TABLE

    daily_inventory_stg2.show() 

    #creating views for final daily fact tables
    sql_table( daily_inventory_stg2, 'final_daily_sale_stg_df')


    #WEEKLY DAILY STAGING TABLE
    weekly_inventory_stg2 = spark.sql(weekly_fact_query) #DAILY INVENTORY STAGING TABLE

    weekly_inventory_stg2.show() 

    #STEP 3 SAVING FILES TO S3

    print("saving file to s3")

    #saving weekly final table partition file to s3 in parquet format

    writing_parquet_files(params, 'output_path', 'partition_column', weekly_inventory_stg2)

    #saving dimension tables partition file to s3 in parquet format

    writing_parquet_files(params, 'output_path1', 'partition_column1', store_dim_df)

    writing_parquet_files(params, 'output_path2', 'partition_column2', product_dim_df)

    writing_parquet_files(params, 'output_path3', 'partition_column3', calendar_dim_df)







  




 

















        
