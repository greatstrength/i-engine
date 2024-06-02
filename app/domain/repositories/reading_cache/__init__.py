from ...constants import *
from ...objects import *

class ReadingCache():

    def save(self, reading: ReadingResult, synced: bool = False):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()

    def get(self, reading_id: str, synced: bool = False) -> ReadingResult:
        raise NotImplementedError()

    def remove(self, reading_id: str):
        raise NotImplementedError()