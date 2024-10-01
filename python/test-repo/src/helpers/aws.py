from typing import Any

import boto3  # type: ignore


class AWS:
    def __init__(self):
        pass

    def store_file_to_s3(self, bucket: str, file_name: str, data: Any) -> None:
        """
        Store any file to AWS S3.

        Args:
            bucket (str): name of the S3 bucket where the file will be stored.
            file_name (str): name of the file, could contain directory name as well.
            data (Any): data that will be stored.
        """
        s3 = boto3.resource("s3")
        s3.Bucket(bucket).put_object(Key=file_name, Body=data)
