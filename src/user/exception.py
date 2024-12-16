from core.exception import BaseCustomException


class UserException:
    UserNotFoundError = BaseCustomException(code=400, detail='User not found')
    PasswordIsShortError = BaseCustomException(code=400, detail='Password is short then 4 chars')
    UserExistsError = BaseCustomException(code=400, detail='User already exists')