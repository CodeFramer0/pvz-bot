from urllib.parse import urlparse

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = getattr(settings, "MINIO_BUCKET_MEDIA", "media")
    default_acl = "private"
    querystring_auth = True

    def url(self, name, parameters=None, expire=None, http_method=None):
        client = self.connection.meta.client
        signed_url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": name},
            ExpiresIn=expire or 3600,
            HttpMethod=http_method or "GET",
        )
        parsed = urlparse(signed_url)
        return f"{settings.PROTOCOL}://media.{settings.MINIO_DOMAIN}/{name.lstrip('/')}?{parsed.query}"


class StaticStorage(S3Boto3Storage):
    bucket_name = getattr(settings, "MINIO_BUCKET_STATIC", "static")
    default_acl = "public-read"
    querystring_auth = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        return (
            f"{settings.PROTOCOL}://static.{settings.MINIO_DOMAIN}/{name.lstrip('/')}"
        )
