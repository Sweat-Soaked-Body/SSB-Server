from core.exception import BaseCustomException


class FriendException:
    UserNotFound = BaseCustomException(code=400, detail='User not found')
    FriendAlreadyExists = BaseCustomException(code=400, detail='Friend already exists')