from schematics import types as t, Model


# Container configuration
class ContainerConfiguration(Model):
    
    monday_api_v2_key = t.StringType(required=True, deserialize_from='MONDAY_API_V2_KEY')


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfiguration):
        # Default init
        self.config = config

        # Custom init below
        # ...
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)
