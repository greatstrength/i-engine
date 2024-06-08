from aikicore.factories.app import *

from ..objects import *
from ..contexts import *
from .cli import *


def create_app(name: str, interface: str, config: dict, container: Container, type: type = CliAppContext) -> AppContext:
    result: CliAppContext = type(name, interface, config, container)

    # Get args cache.
    args_cache = container.args_cache()

    # Create cli parser.
    parser = create_cli_parser(args_cache.list())

    # Set parser.
    result.parser = parser

    return result