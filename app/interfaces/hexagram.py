"""I Ching Engine Interfaces Hexagram"""

# *** imports

# ** core
from abc import abstractmethod
from typing import Dict, List, Optional

# ** app
from tiferet.interfaces import Service

# *** interfaces

# ** interface: hexagram_service
class HexagramService(Service):
    '''
    Service interface for managing I Ching hexagram data.
    '''

    # * method: exists
    @abstractmethod
    def exists(self, number: int) -> bool:
        '''
        Check if a hexagram exists by its Wilhelm number.

        :param number: The hexagram number (1 to 64).
        :type number: int
        :return: True if the hexagram exists.
        :rtype: bool
        '''
        raise NotImplementedError()

    # * method: get
    @abstractmethod
    def get(self, number: int):
        '''
        Retrieve a hexagram by its Wilhelm number.

        :param number: The hexagram number (1 to 64).
        :type number: int
        :return: The hexagram domain object, or None.
        '''
        raise NotImplementedError()

    # * method: list
    @abstractmethod
    def list(self) -> List:
        '''
        List all hexagrams.

        :return: A list of hexagram domain objects.
        :rtype: List
        '''
        raise NotImplementedError()

    # * method: save
    @abstractmethod
    def save(self, hexagram) -> None:
        '''
        Persist a hexagram.

        :param hexagram: The hexagram to save.
        '''
        raise NotImplementedError()

    # * method: search
    @abstractmethod
    def search(self,
            query_embedding: List[float],
            limit: int = 5,
        ) -> List[Dict]:
        '''
        Search hexagrams by embedding similarity.

        :param query_embedding: The query embedding vector.
        :type query_embedding: List[float]
        :param limit: Maximum number of results.
        :type limit: int
        :return: A ranked list of dicts with hexagram number and score.
        :rtype: List[Dict]
        '''
        raise NotImplementedError()
