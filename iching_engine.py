import os
from aikicore import create_app
from aikicore.config import *

from app import *

# Get args
args = cli.arguments

# Pop env from args using default app env if not provided
env = args.args.pop('env', constants.DEFAULT_APP_ENV)

# Pop verbose from args using false if not provided
debug = args.args.pop('verbose', False)

# Preprocess
os.environ[constants.APP_ENV] = env

# Create container.
container_config = IChingContainerConfiguration(dict(os.environ), strict=False)
container = IChingContainer(container_config)

# Get app configuration.
app_config_reader: AppConfigurationReader = load_app_config_reader(
    APP_CONFIGURATION_FILE)
app_config = app_config_reader.load_config(strict=False)

# Create app context.
app_context = create_app('iching_engine', cli.DEFAULT_INTERFACE, app_config, container, type=cli.CliAppContext)

# Run app context.
app_context.run(
    command = args.command,
    function = args.subcommand,
    args=args.args, 
    env=env,
    debug=debug)