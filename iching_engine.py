import os
from aikicore.config import *

from app import *


# Create container.
container = create_container()

# Get arguments cache.
args_cache = container.args_cache()

parser = cli.create_cli_parser(args_cache.list())

# Create command.
command = cli.create_cli_command_execution(parser)

# Get app configuration.
app_config_reader: AppConfigurationReader = load_app_config_reader(
    APP_CONFIGURATION_FILE)
app_config = app_config_reader.load_config(strict=False)

# Create app context.
app_context = cli.create_app('iching_engine', cli.DEFAULT_INTERFACE, app_config, container, type=cli.CliAppContext)

# Run app context.
app_context.run(command=command)