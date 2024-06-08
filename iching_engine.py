import os
from aikicore.config import *

from app import *

command: cli.CliCommandExecution = cli.create_cli_command_execution()

# Preprocess
os.environ[constants.APP_ENV] = command.env

# Create container.
container = create_container()

# Get app configuration.
app_config_reader: AppConfigurationReader = load_app_config_reader(
    APP_CONFIGURATION_FILE)
app_config = app_config_reader.load_config(strict=False)

# Create app context.
app_context = create_app('iching_engine', cli.DEFAULT_INTERFACE, app_config, container, type=cli.CliAppContext)

# Run app context.
app_context.run(command=command)