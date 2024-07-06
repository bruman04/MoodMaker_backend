import boto3
from botocore.exceptions import NoCredentialsError, ClientError
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


# def download(bucket_name, key):
#     s3_client = boto3.client('s3')
#     try:
#         file_obj = s3_client.get_object(Bucket=bucket_name, Key=key)
#         return file_obj
#     except ClientError as e:
#         print(e)
#         return None

def download(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object"""
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None
    return response

def list_all_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
    return contents