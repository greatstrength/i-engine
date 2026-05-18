"""I Ching Engine Hexagram Events"""

# *** imports

# ** core
from typing import List

# ** app
from tiferet.events import DomainEvent

from ..domain.hexagram import Hexagram
from ..domain.constants import HEXAGRAM_NOT_FOUND_ID
from ..interfaces.hexagram import HexagramService

# *** events

# ** event: get_hexagram
class GetHexagram(DomainEvent):
    '''
    Event to retrieve a hexagram by its Wilhelm number.
    '''

    # * attribute: hexagram_service
    hexagram_service: HexagramService

    # * init
    def __init__(self, hexagram_service: HexagramService):
        '''
        Initialize the GetHexagram event.

        :param hexagram_service: The hexagram service.
        :type hexagram_service: HexagramService
        '''

        # Set the hexagram service dependency.
        self.hexagram_service = hexagram_service

    # * method: execute
    @DomainEvent.parameters_required(['number'])
    def execute(self, number: int, **kwargs) -> Hexagram:
        '''
        Retrieve a hexagram by number.

        :param number: The hexagram number (1 to 64).
        :type number: int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The hexagram domain object.
        :rtype: Hexagram
        '''

        # Retrieve the hexagram.
        hexagram = self.hexagram_service.get(int(number))

        # Verify the hexagram exists.
        self.verify(
            expression=hexagram is not None,
            error_code=HEXAGRAM_NOT_FOUND_ID,
            number=number,
        )

        # Return the hexagram.
        return hexagram


# ** event: list_hexagrams
class ListHexagrams(DomainEvent):
    '''
    Event to list all hexagrams.
    '''

    # * attribute: hexagram_service
    hexagram_service: HexagramService

    # * init
    def __init__(self, hexagram_service: HexagramService):
        '''
        Initialize the ListHexagrams event.

        :param hexagram_service: The hexagram service.
        :type hexagram_service: HexagramService
        '''

        # Set the hexagram service dependency.
        self.hexagram_service = hexagram_service

    # * method: execute
    def execute(self, **kwargs) -> List[Hexagram]:
        '''
        List all hexagrams.

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: A list of hexagram domain objects.
        :rtype: List[Hexagram]
        '''

        # Return all hexagrams.
        return self.hexagram_service.list()
