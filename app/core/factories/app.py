from aikicore.factories.app import *
from ..containers import *


def create_container() -> Container:
    import os

    # Create container configuration.
    config = IChingContainerConfiguration(dict(os.environ), strict=False)

    # Return container.
    return IChingContainer(config)
