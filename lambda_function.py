#Created by Joshua Omolewa

#importing required libraries
import json
import boto3
import time  
import subprocess  #library to run external program from this code
import os
from send_email import send_email




def lambda_handler(event, context):
    print()
    s3_file_list = [] #creating an empty list

    s3_client=boto3.client('s3') #establishing s3 connection 
    
    #for loops= to get all the keys present content s3 and append their names to the empty list s3_file_list 
    for object in s3_client.list_objects_v2(Bucket='snowflake-raw-data1')['Contents']:
        s3_file_list.append(object['Key'])
    # print(s3_file_list)
    
    #Setting the correct timezone for our files
    default_date_str = time.strftime("%Y-%m-%d")  #return the local time zone when code is executed in YYY-MM-DD format to match csv files 
    os.environ['TZ'] = 'America/Edmonton'  #change local timezone to edmonton time
    time.tzset()  # tzset() method resets the time conversion rules used by the library routines to new set timezone.
    datestr = time.strftime("%Y-%m-%d") #new edmonton timezone deployed
    #datestr ='2022-12-11'  # use to test if email is working properly
    # print(default_date_str) #checking default date
    # print(datestr) #cheking new date as this matches snoflakes timezone edmonton timezone
    
    
    #the required file list that needs to be processed in s3 bucket (it uses the date the script is run)
    required_file_list = [f'calendar_{datestr}.csv', f'inventory_{datestr}.csv', f'product_{datestr}.csv', f'sales_{datestr}.csv', f'store_{datestr}.csv']
    # print(required_file_list)

     
    # code using for list comprehension for matching raw data file
    matching_files = [x for x in s3_file_list if x in required_file_list]
    
     # scanning S3 bucket to check the required files
    if required_file_list == matching_files:  #this convert require_file_list to set which is unordered and then a list and chek if it matches matching_files 
        #creating a list compression that create a list for the url to the matching require filespresent in the s3_file_list
        s3_file_url = ['s3://' + 'snowflake-raw-data1/' + file for file in matching_files]
        print(s3_file_url)
        """
        creating a list comprehension that create a list for the file name (table name in snowfalkes) 
        in the s3 bucket that matches required list ( this excudes for example "_1999-03-05.csv" which are last 15 charaters)
        """
        table_name = [a[:-15] for a in matching_files]   
        print(table_name) #checking values are correct
        
        #creating a variable that store json object using json.dumps whcih convert dictionary to json object . 
        #The dictionary was created using dictionary comprenhension which has two for loop that create key_value pair of tablename/filename and url
        data = json.dumps({'conf':dict(zip(table_name, s3_file_url))})
        
        # data = json.dumps({'conf':{a:b for a in table_name for b in matching_files}}) #optional method to created disctionary comprehension for data config being sent to airflow
        
        print(data) #checking json data is correct
        # send signal to Airflow  (trigger airflow REST endpoint)  
        endpoint= 'http://54.145.202.197:8080/api/experimental/dags/joshua_project_trigger/dag_runs'
    
        subprocess.run(['curl', '-X', 'POST', endpoint, '--insecure', '--data', data])
        print('File are sent to Airflow')
        
    else:
        print("data files not complete")
        send_email()
    
  
    
            
        
    
    
   




