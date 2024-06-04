import os
from app import *
from app.core import *

# Get args
args = i.args

# Pop env from args using default app env if not provided
env = args.args.pop('env', constants.DEFAULT_APP_ENV)

# Pop verbose from args using false if not provided
debug = args.args.pop('verbose', False)

# Preprocess
os.environ[constants.APP_ENV] = env

# Create builder
builder = i.CliAppBuilder().create_new_app('kabbalapp')

# Set container configuration to builder
container_config = IChingContainerConfiguration(dict(os.environ), strict=False)
builder.set_container_config(container_config)

# Build app context.
app_context: i.CliAppContext = builder.build(container=IChingContainer)

# Run app context.
app_context.run(
    command = args.command,
    function = args.subcommand,
    args=args.args, 
    env=env,
    debug=debug)