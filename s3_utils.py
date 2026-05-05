import boto3
import os

def get_s3_client():
    return boto3.client('s3', region_name='us-east-1')

BUCKET_NAME = 'ecommerce-pipeline-jeet'

def upload_file(local_path, s3_key):
    s3 = get_s3_client()
    s3.upload_file(local_path, BUCKET_NAME, s3_key)
    print(f"Uploaded {local_path} to s3://{BUCKET_NAME}/{s3_key}")

def download_file(s3_key, local_path):
    s3 = get_s3_client()
    s3.download_file(BUCKET_NAME, s3_key, local_path)
    print(f"Downloaded s3://{BUCKET_NAME}/{s3_key} to {local_path}")