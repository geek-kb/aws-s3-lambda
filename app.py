# Code by Itai Ganot 2021

import boto3
import os
import json
from botocore.exceptions import ClientError


def send_email(bucket_name, file_name, file_type, url):
    email_address = os.environ['email_address']
    user_name = os.environ['user_name']
    region = os.environ['region']
    SENDER = "{} <{}>".format(user_name, email_address)
    RECIPIENT = "{}".format(email_address)
    SUBJECT = "A new file has been uploaded to S3 bucket {}".format(bucket_name)
    BODY_TEXT = ("The following file has been uploaded to bucket: {}\nFile Name: {}\nFile Type: {}".format(bucket_name, file_name, file_type))
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>File type checker</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
        <br>
        The following file has been uploaded to bucket: {}
        <br>
        File Name: {}
        <br>
        File Type: {}
        <br>
        URL: {}
        <br>
    </body>
    </html>
    """.format(bucket_name, file_name, file_type, url)
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=region)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
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
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def lambda_handler(event, context):
    print(json.dumps(event,indent=4,default=str))
    info = event['Records'][0]['s3']
    file_name = info['object']['key']
    bucket_name = info['bucket']['name']
    
    s3_client = boto3.client('s3')
    location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = "https://s3-{}.amazonaws.com/{}/{}".format(location, bucket_name, file_name)
    response = s3_client.head_object(Bucket=bucket_name, Key=file_name)
    file_type = response['ContentType'].replace('application/', '')
    print('info: {}, file_name: {}, bucket_name: {}'.format(info, file_name, bucket_name))
    send_email(bucket_name, file_name, file_type, url)

