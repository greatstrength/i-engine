from typing import Any
from .constants import *

from schematics import types as t, Model

# Container configuration


class ContainerConfiguration(Model):

    monday_api_v2_key = t.StringType(deserialize_from='MONDAY_API_V2_KEY')
    hexagram_board_id = t.StringType(deserialize_from='HEXAGRAM_BOARD_ID')
    reading_board_id = t.StringType(deserialize_from='READING_BOARD_ID')
    cache_path = t.StringType(
        required=True, deserialize_from='CACHE_PATH', default=YAML_CACHE_PATH)
    hexagram_cahce_path = t.StringType(
        required=True, deserialize_from='HEXAGRAM_CACHE_PATH', default=YAML_HEXAGRAM_CACHE_PATH)


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfiguration):
        # Default init
        self.config = config

        # Custom init below
        # ...

    def monday_client(self):
        from mondata import client
        client.api_key = self.config.monday_api_v2_key
        return client

    def reading_cache(self):
        from app.domain.repositories.reading_cache.yaml import YamlReadingCache
        return YamlReadingCache(self.config.cache_path)

    def hexagram_cache(self):
        from app.domain.repositories.hexagram.yaml import HexagramYamlRepository
        return HexagramYamlRepository(self.config.hexagram_cahce_path)

    def reading_repo(self):
        from app.domain.repositories.reading.mondata import MondataReadingRepository
        return MondataReadingRepository(
            self.monday_client(),
            self.config.reading_board_id
        )

    def hexagram_repo(self):
        from app.domain.repositories.hexagram.mondata import MondataHexagramRepository
        return MondataHexagramRepository(
            self.monday_client(),
            self.config.hexagram_board_id
        )

# Default dynamic container


class DynamicContainer():

    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)
