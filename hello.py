import boto3
import requests
import os

AWS_ACCESS_KEY=os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Fetch the list of existing buckets
clientResponse = client.list_buckets()

'''
# Upload a new file
data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)
'''

def list_s3():
    for bucket in clientResponse['Buckets']:
        print(f'Bucket Name: {bucket["Name"]}')

if __name__ == "__main__":
    print("Running script")
    list_s3()
