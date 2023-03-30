import boto3
from botocore.exceptions import ClientError #for error handling

def send_email():
    
    # This address must be verified with Amazon SES.
    SENDER = "omolewa.joshua1@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "omolewa.joshua1@gmail.com"


    # using east-1 If necessary, replace with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "snowflake-raw-data1 bucket"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Files missing in AWS S3 bucket. Please check Snowflake task.")



    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email. and using error handling with client e
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER

        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])