from core.exception import BaseCustomException


class UserException:
    UserNotFoundError = BaseCustomException(code=400, detail='User not found')