from ... import *
from ..objects import *

def create_cli_command_execution():
    import sys, argparse
    import yaml
    import json

    from ..config import CliInterfaceConfiguration


    with open('app/app.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())

    # Get app interface types
    interfaces = app_config.get('interfaces', None)
    types = interfaces.get('types', None)

    # Print a message if no interface types are configured
    if types is None:
        print('No interfaces configured.')
        sys.exit(0)
    # Get cli interface
    cli_interface = types.get('cli', None)
    # Print a message if not cli interface is configured
    if cli_interface is None:
        print('No cli interface configured.')
        sys.exit(0)

    cli_interface = CliInterfaceConfiguration(cli_interface)

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add command subparsers
    command_subparsers = parser.add_subparsers(dest='command')
    for command_name, command in cli_interface.commands.items():
        command_name = command_name.replace('_', '-')
        command_subparser = command_subparsers.add_parser(command_name, **command.to_primitive('add_parser'))
        subcommand_subparsers = command_subparser.add_subparsers(dest='subcommand')
        for subcommand_name, subcommand in command.subcommands.items():
            subcommand_name = subcommand_name.replace('_', '-')
            subcommand_subparser = subcommand_subparsers.add_parser(subcommand_name, help=subcommand.help)
            for argument in subcommand.arguments:
                subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))
            for argument in cli_interface.parent_arguments:
                subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))

    # Parse arguments.
    args = parser.parse_args()
    args = vars(args)
    command = args.pop('command').replace('-', '_')
    function = args.pop('subcommand').replace('-', '_')
    env = args.pop('env', DEFAULT_APP_ENV)
    debug = args.pop('verbose', False)

    return CliCommandExecution(dict(
        command=command,
        function=function,
        args=json.dumps(args),
        env=env,
        debug=debug
    ), strict=False)