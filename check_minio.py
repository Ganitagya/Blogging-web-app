"""
Quick script to verify Minio credentials and permissions.

Run with: uv run check_minio.py

This checks that your .env credentials can upload to and delete from your S3 bucket
without needing to go through the full application flow.
"""

from io import BytesIO

from botocore.exceptions import BotoCoreError, ClientError

from config import settings
from image_utils import _get_s3_client


def check_s3_connection():
    s3 = _get_s3_client()

    print(f"Bucket: {settings.minio_bucket_name}")
    print(f"Region: {settings.minio_region}")
    print()

    test_key = "profile_pics/test.txt"

    # Test upload
    try:
        s3.upload_fileobj(
            BytesIO(b"test"),
            settings.minio_bucket_name,
            test_key,
            ExtraArgs={"ContentType": "text/plain"},
        )
        print("Upload: SUCCESS")
    except (BotoCoreError, ClientError) as e:
        print(f"Upload: FAILED - {e}")
        return

    # Test delete
    try:
        s3.delete_object(Bucket=settings.minio_bucket_name, Key=test_key)
        print("Delete: SUCCESS")
    except (BotoCoreError, ClientError) as e:
        print(f"Delete: FAILED - {e}")
        return

    print()
    print("All tests passed! Your Minio configuration is working.")


def check_object_exists(object_key: str) -> bool:
    s3 = _get_s3_client()

    try:
        s3.head_object(
            Bucket=settings.minio_bucket_name,
            Key=object_key,
        )
        return True

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")

        if error_code in ("404", "NoSuchKey", "NotFound"):
            return False

        raise

    except BotoCoreError:
        raise

if __name__ == "__main__":
    check_s3_connection()

    object_key = "profile_pics/b50cbbf5a8264dedace58121804dfdff.jpg"

    if check_object_exists(object_key):
        print("Object exists")
    else:
        print("Object not found")