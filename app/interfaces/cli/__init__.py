from ...core import *
from ...features import *

INTERFACE = 'cli'

class CliAppContext(AppContext):

    def run(self, **kwargs):
        from importlib import import_module

        # Remove necessary arguments
        command = kwargs.pop('command')
        function = kwargs.pop('function')
        args = kwargs.pop('args')

        
        # Load endpoint configuration.
        
        
        # Create endpoint handler.
        handler = import_module(
            DEFAULT_EXECUTE_FEATURE_HANDLER_PATH)
        
        # Handle message context.
        try:
            result = handler.handle(request=args, app_context=self, feature_id='{}.{}'.format(command, function), **kwargs)
        except AppError as e:
            exit(str(e.to_dict()))

        # Print result if not empty.
        if result:
            import json
            print(json.dumps(result, indent=4, sort_keys=True))


class CliAppBuilder(AppBuilder):
    
    def build(self, container: type = Container):
        return CliAppContext(
            self._current_session.name,
            INTERFACE,
            self._current_session.app_config,
            self._current_session.container_config,
            container
        )
