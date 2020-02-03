import boto3

from commons.config import AWS


def get_email_from_path(path):
    return path.split('/')[0]


def make_file_public_for_download(bucket, key, region=AWS['region']):
    s3 = boto3.client('s3')
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)
    return f'http://s3.amazonaws.com/{bucket}/{key}'
