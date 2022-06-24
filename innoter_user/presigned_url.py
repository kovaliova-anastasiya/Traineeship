import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
# from innoter.settings import AWS_ACCESS_KEY_ID, \
#     AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

s3_signature = {
    'v4': 's3v4',
    'v2': 's3'
}

AWS_ACCESS_KEY_ID = 'AKIAVS5XG7RWM2EHXBW4'
AWS_SECRET_ACCESS_KEY = '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'
AWS_DEFAULT_REGION = 'us-east-1'


def create_presigned_url(bucket_name, bucket_key, expiration=3600, signature_version=s3_signature['v4']):
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             config=Config(signature_version=signature_version),
                             region_name=AWS_DEFAULT_REGION
                             )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': bucket_key},
                                                    ExpiresIn=expiration)
        # print(s3_client.list_buckets()['Owner'])

    except ClientError as e:
        logging.error(e)
        return None
    return response
