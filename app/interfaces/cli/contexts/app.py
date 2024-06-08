from aikicore.contexts.app import *
from aikicore.errors import *
from aikicore.errors import AppError
from aikicore.objects import Error
from ..objects import *


class CliAppContext(AppContext):

    parser = None

    def map_feature_request(self, command: CliCommandExecution) -> ExecuteFeature:
        return ExecuteFeature(dict(
            feature_id='{}.{}'.format(command.command, command.function),
            data=command.args,
            **command.to_primitive()
        ), strict=False)

    def map_headers(self, command: CliCommandExecution) -> Header:
        return IChingCliHeader(dict(
            command=command.command,
            function=command.function,
            env=command.env,
        ))

    def map_response(self, result):

        # Perform base mapping.
        result = super().map_response(result)

        # Decoration.
        if result:
            import json
            print(json.dumps(result, indent=4, sort_keys=True))

    def handle_error(self, error: AppError, lang: str = 'en_US', error_type: type = Error, **kwargs):
        error = super().handle_error(error, lang, error_type, **kwargs)
        exit(str(dict(
            error_name=error.error_name,
            error_code=error.error_code,
            message=error.message,
        )))

    def run(self, command: CliCommandExecution, **kwargs):

        # Map request.
        request = self.map_feature_request(command)

        # Map headers.
        headers = self.map_headers(command)

        # Handle message context.
        try:
            response = self.get_feature_handler().handle(
                request=request,
                app_context=self,
                headers=headers,
                **kwargs)
        except Exception as e:
            if isinstance(e, AppError):
                self.handle_error(e, **kwargs)

        # Get result.
        self.map_response(response.result)
