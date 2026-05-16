"""I Ching Engine Interfaces Reading"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List, Optional

# ** app
from tiferet.interfaces import Service

# *** interfaces

# ** interface: reading_service
class ReadingService(Service):
    '''
    Service interface for managing I Ching readings.
    '''

    # * method: exists
    @abstractmethod
    def exists(self, id: str) -> bool:
        '''
        Check if a reading exists by ID.

        :param id: The reading identifier.
        :type id: str
        :return: True if the reading exists.
        :rtype: bool
        '''
        raise NotImplementedError()

    # * method: get
    @abstractmethod
    def get(self, id: str):
        '''
        Retrieve a reading by ID.

        :param id: The reading identifier.
        :type id: str
        :return: The reading domain object, or None.
        '''
        raise NotImplementedError()

    # * method: list
    @abstractmethod
    def list(self,
            reading_type: Optional[str] = None,
            frequency: Optional[str] = None,
            date: Optional[str] = None,
        ) -> List:
        '''
        List readings with optional filters.

        :param reading_type: Optional reading type filter.
        :type reading_type: str | None
        :param frequency: Optional frequency filter.
        :type frequency: str | None
        :param date: Optional date filter (ISO format).
        :type date: str | None
        :return: A list of reading domain objects.
        :rtype: List
        '''
        raise NotImplementedError()

    # * method: save
    @abstractmethod
    def save(self, reading) -> None:
        '''
        Persist a reading.

        :param reading: The reading to save.
        '''
        raise NotImplementedError()

    # * method: delete
    @abstractmethod
    def delete(self, id: str) -> None:
        '''
        Delete a reading by ID.

        :param id: The reading identifier.
        :type id: str
        '''
        raise NotImplementedError()
