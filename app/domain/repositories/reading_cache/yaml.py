from . import *

import yaml


class YamlReadingCache(ReadingCache):

    def __init__(self, cache_path: str):
        self.cache_path = cache_path

    def save(self, reading: ReadingResult, synced: bool = False):
        with open(self.cache_path, 'r') as f:
            readings = yaml.safe_load(f)
            if readings is None:
                readings = {}
            reading_data = reading.to_primitive()
            key = reading_data.pop('id')
            reading_data['synced'] = synced
            readings[key] = reading_data

        with open(self.cache_path, 'w') as f:
            yaml.dump(readings, f)

    def list(self):
        with open(self.cache_path, 'r') as f:
            readings = yaml.safe_load(f)
            if readings is None:
                readings = []
        return [
            ReadingResult(dict(
                id=key,
                **value
            ), strict=False)
            for key, value in readings.items()
        ]

    def get(self, reading_id: str) -> ReadingResult:
        with open(self.cache_path, 'r') as f:
            readings: Dict = yaml.safe_load(f)
            if readings is None:
                return None
            reading_data = readings.get(reading_id, None)
            if reading_data is None:
                return None
            return ReadingResult(dict(**reading_data, id=reading_id), strict=False)

    def remove(self, reading_id: str):
        with open(self.cache_path, 'r') as f:
            readings = yaml.safe_load(f)
            if readings is None:
                readings = {}
            if reading_id in readings:
                del readings[reading_id]

        with open(self.cache_path, 'w') as f:
            yaml.dump(readings, f)
