import boto3
from botocore.exceptions import ClientError

# Environment variables
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class AWSProvider:
    def upload_file_s3(self, path_to_save, path_to_file, bucket=env("BUCKET_NAME")):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=env("ACCESS_KEY"),
            aws_secret_access_key=env("SECRET_ACCESS_KEY"),
        )
        try:
            s3_client.upload_file(path_to_file, bucket, Key=path_to_save)
            url = s3_client.generate_presigned_url(
                "get_object",
                ExpiresIn=0,
                Params={"Bucket": bucket, "Key": path_to_save},
            )
            return str(url).split("?")[0]
        except ClientError as error:
            print(error)
            return False

    def delete_file(self, path):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=env("ACCESS_KEY"),
            aws_secret_access_key=env("SECRET_ACCESS_KEY"),
        )
        bucket=env("BUCKET_NAME")
        try:
            s3_client.delete_object(Bucket=bucket, Key=path)
            return True
        except ClientError as error:
            print(error)
            return False
