from ...constants import *
from ...objects import *


class ReadingRepository():

    def save(self, reading: ReadingResult):
        pass

    def save_result_data(self, reading_id: str, result_data: List[ResultLine]):
        raise NotImplementedError()

    def set_hexagrams(self, reading_id: str, hexagram_id: str, changing_hexagram_id: str = None):
        raise NotImplementedError()
    
    def upload_entry(self, reading_id: str, upload_file: str):
        raise NotImplementedError()
