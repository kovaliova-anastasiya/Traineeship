import logging
import boto3
from botocore.exceptions import ClientError

s3_signature = {
    'v4': 's3v4',
    'v2': 's3'
}


def create_presigned_url(bucket_name, bucket_key, expiration=3600, signature_version=s3_signature['v4']):
    s3_client = boto3.client('s3')

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
