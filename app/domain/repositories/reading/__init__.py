from ...constants import *
from ...objects import *


class ReadingRepository():

    def save(self, reading: ReadingResult):
        pass

    def set_hexagrams(self, reading_id: str, hexagram_id: str, changing_hexagram_id: str = None):
        raise NotImplementedError()
