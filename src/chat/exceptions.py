from core.exception import BaseCustomException


class MessageException:
    MessageNotFoundError = BaseCustomException(code=400, detail='Message not found')