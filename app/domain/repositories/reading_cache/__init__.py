from ...constants import *
from ...objects import *

class ReadingCache():

    def save(self, reading: ReadingResult):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()

    def get(self, reading_id: str) -> ReadingResult:
        raise NotImplementedError()