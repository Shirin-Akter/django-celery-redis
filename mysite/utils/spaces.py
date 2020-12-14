import boto3
import os
import time
from datetime import datetime
from django.conf import settings
#import botocore
from botocore.exceptions import ClientError

from urllib.parse import urlsplit, urlunsplit

space_name="xrl"

def space_connect():
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=settings.AWS_DEFAULT_REGION,
                            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return client

def list_spaces():
    response = space_connect().list_buckets()
    print(response)
    for space in response['Buckets']:
        print(space['Name'])

def list_files(dir):
    try:
        response = space_connect().list_objects(Bucket=space_name, Prefix=dir)
        for obj in response['Contents']:
            print(obj['Key'])
    except Exception as e:
        print(str(e))
  
def download_file(file_name):
    try:
        file_path = os.path.basename(file_name)
        print(file_path)
        space_connect().download_file(space_name, file_name, file_path)
    except Exception as e:
        print(str(e))

def upload_file(file_path):
    file_name = os.path.basename(file_path)
    try:
        space_connect().upload_file(file_path, space_name, file_name)
        space_connect().put_object_acl(ACL='public-read', Bucket=space_name, Key=file_name)
    except Exception as e:
        print(str(e))

def delete_file(file_path):
    try:
        space_connect().delete_object(Bucket=space_name, Key=file_path)
        print("File deleted")
    except:
        print("File does not exist")

def delete_folder(dir):
    s3 = space_connect()
    objects = s3.list_objects(Bucket=space_name, Prefix=dir)
    objects_to_delete = []
    try:
        for obj in objects['Contents']:
            objects_to_delete.append({'Key': obj['Key']})

        response = s3.delete_objects(Bucket=space_name,
                                        Delete={
                                            'Objects': objects_to_delete
                                        })
        print("Deleted: {0}".format(response['Deleted']))
    except:
        print("Folder does not exist.")

def create_read_url(bucket_name, object_name, expiration=3600):
   
    s3 = space_connect()
    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': bucket_name,
                                            'Key': object_name},
                                    ExpiresIn=expiration)
    urls = list(urlsplit(url))
    urls[1]=settings.CDN_HOST
    return  urlunsplit(urls)


def create_write_url(bucket_name, object_name=None, acl=None, expiration=3600):
   
    s3 = space_connect()
    if acl:
        params = {'Bucket': bucket_name, 'Key': object_name, 'ACL':acl}
    else:
        params = {'Bucket': bucket_name, 'Key': object_name}
    return s3.generate_presigned_url('put_object',
                                        Params=params,
                                        ExpiresIn=expiration)
