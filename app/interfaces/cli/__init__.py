from ...core import *
from ...features import *
from .objects import *

INTERFACE = 'cli'


class CliAppContext(AppContext):

    def map_feature_request(self, request):
        import json

        command = request.get('command')
        function = request.get('function')
        data = request.pop('args', None)
        data = json.dumps(data) if data else None
        feature_id = '{}.{}'.format(command, function)

        return ExecuteFeature(dict(
            feature_id=feature_id,
            data=data,
            **request,
        ), strict=False)

    def map_headers(self, request) -> Header:
        return IChingCliHeader(
            request,
            strict=False
        )

    def map_response(self, result):

        # Perform base mapping.
        result = super().map_response(result)

        # Decoration.
        if result:
            import json
            print(json.dumps(result, indent=4, sort_keys=True))

    def run(self, **kwargs):

        # Map request.
        request = self.map_feature_request(kwargs)

        # Map headers.
        headers = self.map_headers(kwargs)

        # Handle message context.
        try:
            response = self.get_feature_handler().handle(
                request=request,
                app_context=self,
                headers=headers,
                **kwargs)
        except AppError as e:
            exit(str(e.to_dict()))

        # Get result.
        self.map_response(response.result)


class CliAppBuilder(AppBuilder):

    def build(self, container: type = Container):
        return CliAppContext(
            self._current_session.name,
            INTERFACE,
            self._current_session.app_config,
            self._current_session.container_config,
            container
        )
