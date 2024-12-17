from core.exception import BaseCustomException


class AWSException:
    S3UploadFailError = BaseCustomException(code=500, detail='s3 upload fail')
    InvalidImageTypeError = BaseCustomException(code=500, detail='invalid image type')