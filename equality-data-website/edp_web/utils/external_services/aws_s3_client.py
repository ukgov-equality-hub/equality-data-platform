import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config


class AwsS3Client:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client(
            's3',
            region_name="eu-west-2",
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = bucket_name


    def download_object(self, object_name):
        print('Downloading %s' % object_name, flush=True)
        try:
            file = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
            return file['Body'].read()

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)
            return None


    def list_objects(self):
        data = []
        try:
            for key in self.s3.list_objects(Bucket=self.bucket_name)['Contents']:
                data.append(key['Key'])

        except ClientError as e:
            logging.error(e)
            print(e, flush=True)
            return None

        return data
