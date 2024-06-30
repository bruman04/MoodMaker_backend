import boto3
from botocore.exceptions import NoCredentialsError
import requests
import mimetypes


def upload(file_obj, bucket, file_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file_obj, bucket, file_name)
        print("Upload Successful")
        return True
    
    except FileNotFoundError:
        print("The file was not found")
        return False
    
    except NoCredentialsError:
        print("Credentials not available")
        return False


def download(file_name, bucket):
    s3 = boto3.resource('s3')
    output = f"download_files/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)
    return output


def list_all_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
    return contents