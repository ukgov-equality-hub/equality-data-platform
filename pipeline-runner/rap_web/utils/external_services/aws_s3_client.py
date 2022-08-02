import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from rap_web.utils.config_helper import ConfigHelper


class AwsS3Client:
    def __init__(self, instance_name: str):
        buckets = ConfigHelper.get_vcap_services().aws_s3_bucket
        bucket_with_name = next(filter(lambda bucket: bucket.instance_name == instance_name, buckets), None)
        creds = bucket_with_name.credentials

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=creds.aws_access_key_id,
            aws_secret_access_key=creds.aws_secret_access_key,
            region_name=creds.aws_region,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = creds.bucket_name


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
