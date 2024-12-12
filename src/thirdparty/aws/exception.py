from core.exception import BaseCustomException


class AWSException:
    S3UploadFailError = BaseCustomException(code=500, detail='s3 upload fail')