import boto3
import os

AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'eu-central-1')
aws_access_key_id = os.getenv('aws_access_key_id', None)
aws_secret_access_key = os.getenv('aws_secret_access_key', None)
aws_session_token = os.getenv('aws_session_token', None)


class S3Con:

    def __init__(self):
        if aws_access_key_id is not None and aws_secret_access_key is not None and aws_session_token is not None:
            self.resource = boto3.resource('s3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token
            )
        else:
            self.resource = boto3.resource('s3')

    def upload_file_to_s3(self, file_name, bucket, key):
        try:
            s3 = self.resource
            s3.meta.client.upload_file(file_name, bucket, key)
            return True
        except Exception:
            raise Exception
