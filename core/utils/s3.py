import json

import boto3
from botocore.client import Config
from django.conf import settings


# boto3 doc
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html


API_CONNECTION_DICT = {
    "endpoint_url": settings.S3_ENDPOINT,
    "aws_access_key_id": settings.S3_ACCESS_KEY,
    "aws_secret_access_key": settings.S3_SECRET_KEY,
    "region_name": settings.S3_BUCKET_REGION,
    "config": Config(signature_version="s3v4"),
}

DEFAULT_CORS_CONFIGURATION = {
    "CORSRules": [
        {
            "AllowedHeaders": [
                "Cache-Control",
                "x-requested-with",
            ],
            "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
            "AllowedOrigins": settings.CORS_ORIGIN_WHITELIST,
            "ExposeHeaders": ["ETag", "Location"],
        }
    ]
}

DEFAULT_POLICY_CONFIGURATION = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"{settings.S3_BUCKET_NAME}/*",
        },
        {
            "Sid": "DenyPublicUpdate",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": f"{settings.S3_BUCKET_NAME}/*",
        },
        {
            "Sid": "DenyPublicDelete",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:DeleteObject",
            "Resource": f"{settings.S3_BUCKET_NAME}/*",
        },
    ],
}

CONTENT_TYPE_MAPPING = {
    "png": "image/png",
    "PNG": "image/png",
    "svg": "image/svg+xml",
    "gif": "image/gif",
    "jpg": "image/jpg",
    "JPG": "image/jpg",
    "jpeg": "image/jpeg",
}  # "jfif"


client = boto3.client("s3", **API_CONNECTION_DICT)
resource = boto3.resource("s3", **API_CONNECTION_DICT)
bucket = resource.Bucket(settings.S3_BUCKET_NAME)


def get_bucket(bucket_name=settings.S3_BUCKET_NAME):
    bucket = resource.Bucket(bucket_name)
    return bucket


def list_bucket_objects(bucket):
    for obj in bucket.objects.all():
        print(obj.__dict__)


def get_object_metadata(bucket, object_key):
    return client.head_object(Bucket=bucket.name, Key=object_key)


def get_object_url(bucket, object_key):
    return f"{API_CONNECTION_DICT['endpoint_url']}/{bucket.name}/{object_key}"


def upload_object(bucket, object_file_path, s3_object_key):
    """
    in read-mode instead of download-mode: https://stackoverflow.com/a/58641574/4293684
    # alternative
    resource.meta.client.upload_file(object_file_path, bucket_name, s3_file_key, ExtraArgs={"ACL": "public-read", "ContentType": "image/png"})  # noqa
    """
    object_extension = object_file_path.split(".")[1]
    bucket.upload_file(
        object_file_path,
        s3_object_key,
        ExtraArgs={"ACL": "public-read", "ContentType": CONTENT_TYPE_MAPPING[object_extension]},
    )


def delete_object(bucket, object_key):
    bucket.delete_objects(Delete={"Objects": [{"Key": object_key}]})


def delete_all_objects(bucket, prefix=None):
    if prefix:
        # Delete all objects inside a 'folder'
        bucket.objects.filter(Prefix="myprefix/").delete()
    else:
        bucket.objects.delete()


def get_bucket_cors(bucket):
    response = client.get_bucket_cors(Bucket=bucket.name)
    print(response["CORSRules"])


def update_bucket_cors(bucket, cors_configuration=DEFAULT_CORS_CONFIGURATION):
    client.put_bucket_cors(Bucket=bucket.name, CORSConfiguration=cors_configuration)


def get_bucket_policy(bucket):
    response = client.get_bucket_policy(Bucket=bucket.name)
    print(response["Policy"])


def update_bucket_policy(bucket, policy_configuration=DEFAULT_POLICY_CONFIGURATION):
    client.put_bucket_policy(Bucket=bucket.name, Policy=json.dumps(policy_configuration))
