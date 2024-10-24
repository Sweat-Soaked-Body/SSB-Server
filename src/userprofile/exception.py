from core.exception import BaseCustomException


class UserProfileException:
    ProfileAlreadyExists = BaseCustomException(code=400, detail='Profile already exists')