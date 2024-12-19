import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage

from storage.exception import AWSException


class S3Manager:
    @staticmethod
    def upload(image):
        name, extension = os.path.splitext(image.name)
        try:
            path = f'{str(uuid.uuid4())}{extension}'
            join_path = os.path.join(settings.IMAGE_ROOT, path)
            save = default_storage.save(join_path, image)
            s3_path = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{save}'
        except Exception as e:
            # Todo - Logging
            raise AWSException.S3UploadFailError

        return s3_path