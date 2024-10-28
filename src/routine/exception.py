from core.exception import BaseCustomException


class RoutineException:
    RoutineNotFound = BaseCustomException(code=404, detail='Routine not found')

class SetsException:
    SetsNotFound = BaseCustomException(code=404, detail='Sets not found')