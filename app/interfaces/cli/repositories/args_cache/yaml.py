from . import *


def load_cache(cache_path: str):
    import yaml
    from ...config import CliInterfaceConfiguration

    with open(cache_path, 'r') as f:
        app_config = yaml.safe_load(f)

    # Get app interface types
    interfaces = app_config.get('interfaces', None)
    types = interfaces.get('types', None)

    # Print a message if no interface types are configured
    if types is None:
        return None
    # Get cli interface
    cli_interface = types.get('cli', None)
    # Print a message if not cli interface is configured
    if cli_interface is None:
        return None

    cli_interface = CliInterfaceConfiguration(cli_interface)

    cache['cli'] = cli_interface