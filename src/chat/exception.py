from core.exception import BaseCustomException


class RoomException:
    RoomNotFound = BaseCustomException(code=400, detail='Room not found')
