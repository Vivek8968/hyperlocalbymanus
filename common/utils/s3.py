import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from typing import Optional
from ..config.settings import get_settings

settings = get_settings()

class S3Service:
    """
    Service for interacting with AWS S3
    """
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_BUCKET_NAME
    
    async def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for uploading a file to S3
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name,
                    'ContentType': 'application/octet-stream'
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating presigned URL: {str(e)}"
            )
    
    async def get_object_url(self, object_name: str) -> str:
        """
        Get the URL for an object in S3
        """
        return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{object_name}"
    
    async def delete_object(self, object_name: str) -> bool:
        """
        Delete an object from S3
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            return True
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting object: {str(e)}"
            )
