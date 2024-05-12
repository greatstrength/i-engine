from .constants import *

from schematics import types as t, Model

# Container configuration
class ContainerConfiguration(Model):
    
    monday_api_v2_key = t.StringType(required=True, deserialize_from='MONDAY_API_V2_KEY')
    cache_path = t.StringType(required=True, deserialize_from='CACHE_PATH', default=YAML_CACHE_PATH)


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfiguration):
        # Default init
        self.config = config

        # Custom init below
        # ...

    def reading_cache(self, flag: str = 'yaml'):
        
        def yaml():
            from app.domain.repositories.reading_cache.yaml import YamlReadingCache
            return YamlReadingCache(self.config.cache_path)
        
        if flag == 'yaml':
            return yaml()
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)
