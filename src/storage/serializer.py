import os

from rest_framework import serializers

from storage.exception import AWSException
from storage.s3 import S3Manager


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, data):
        name, extension = os.path.splitext(data['file'].name)
        if extension.lower() not in ['.jpg', '.jpeg', '.png']:
            raise AWSException.InvalidImageTypeError

        if data['file'].content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
            raise AWSException.InvalidImageTypeError
        return data

    def upload(self):
        return S3Manager.upload(self.validated_data['file'])