"""I Ching Engine Reading Events"""

# *** imports

# ** core
from typing import List, Optional

# ** app
from tiferet.events import DomainEvent

from ..domain.reading import Reading, ResultLine, HexagramResult
from ..domain.constants import READING_NOT_FOUND_ID
from ..interfaces.reading import ReadingService

# *** events

# ** event: save_reading
class SaveReading(DomainEvent):
    '''
    Event to build and persist a new reading.
    '''

    # * attribute: reading_service
    reading_service: ReadingService

    # * init
    def __init__(self, reading_service: ReadingService):
        '''
        Initialize the SaveReading event.

        :param reading_service: The reading service.
        :type reading_service: ReadingService
        '''

        # Set the reading service dependency.
        self.reading_service = reading_service

    # * method: execute
    @DomainEvent.parameters_required(['name', 'dimension'])
    def execute(self,
            name: str,
            dimension: str,
            frequency: str = 'daily',
            type: str = 'general',
            result_lines: list = None,
            current_or_previous: dict = None,
            next: dict = None,
            **kwargs,
        ) -> Reading:
        '''
        Build and persist a new reading.

        :param name: The reading name.
        :type name: str
        :param dimension: The dimension number for result line calculation.
        :type dimension: str
        :param frequency: The periodic frequency of the reading.
        :type frequency: str
        :param type: The type of reading.
        :type type: str
        :param result_lines: Optional list of result line dicts.
        :type result_lines: list | None
        :param current_or_previous: Optional current/previous hexagram dict.
        :type current_or_previous: dict | None
        :param next: Optional next hexagram dict.
        :type next: dict | None
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The persisted reading domain object.
        :rtype: Reading
        '''

        # Build result line objects.
        lines = [ResultLine(**rl) for rl in (result_lines or [])]

        # Build hexagram references.
        cp = HexagramResult(**current_or_previous) if current_or_previous else None
        nx = HexagramResult(**next) if next else None

        # Construct the reading (id, date, created_at auto-derived).
        reading = Reading(
            name=name,
            dimension=dimension,
            frequency=frequency,
            type=type,
            result_lines=lines,
            current_or_previous=cp,
            next=nx,
        )

        # Persist via the service.
        self.reading_service.save(reading)

        # Return the reading.
        return reading


# ** event: get_reading
class GetReading(DomainEvent):
    '''
    Event to retrieve a reading by its identifier.
    '''

    # * attribute: reading_service
    reading_service: ReadingService

    # * init
    def __init__(self, reading_service: ReadingService):
        '''
        Initialize the GetReading event.

        :param reading_service: The reading service.
        :type reading_service: ReadingService
        '''

        # Set the reading service dependency.
        self.reading_service = reading_service

    # * method: execute
    @DomainEvent.parameters_required(['id'])
    def execute(self, id: str, **kwargs) -> Reading:
        '''
        Retrieve a reading by ID.

        :param id: The reading identifier.
        :type id: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The reading domain object.
        :rtype: Reading
        '''

        # Retrieve the reading.
        reading = self.reading_service.get(id)

        # Verify the reading exists.
        self.verify(
            expression=reading is not None,
            error_code=READING_NOT_FOUND_ID,
            id=id,
        )

        # Return the reading.
        return reading


# ** event: list_readings
class ListReadings(DomainEvent):
    '''
    Event to list readings with optional filters.
    '''

    # * attribute: reading_service
    reading_service: ReadingService

    # * init
    def __init__(self, reading_service: ReadingService):
        '''
        Initialize the ListReadings event.

        :param reading_service: The reading service.
        :type reading_service: ReadingService
        '''

        # Set the reading service dependency.
        self.reading_service = reading_service

    # * method: execute
    def execute(self,
            reading_type: str = None,
            frequency: str = None,
            date: str = None,
            **kwargs,
        ) -> List[Reading]:
        '''
        List readings with optional filters.

        :param reading_type: Optional reading type filter.
        :type reading_type: str | None
        :param frequency: Optional frequency filter.
        :type frequency: str | None
        :param date: Optional date filter (ISO format).
        :type date: str | None
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: A list of reading domain objects.
        :rtype: List[Reading]
        '''

        # Delegate to the reading service.
        return self.reading_service.list(
            reading_type=reading_type,
            frequency=frequency,
            date=date,
        )


# ** event: delete_reading
class DeleteReading(DomainEvent):
    '''
    Event to delete a reading by its identifier.
    '''

    # * attribute: reading_service
    reading_service: ReadingService

    # * init
    def __init__(self, reading_service: ReadingService):
        '''
        Initialize the DeleteReading event.

        :param reading_service: The reading service.
        :type reading_service: ReadingService
        '''

        # Set the reading service dependency.
        self.reading_service = reading_service

    # * method: execute
    @DomainEvent.parameters_required(['id'])
    def execute(self, id: str, **kwargs) -> None:
        '''
        Delete a reading by ID.

        :param id: The reading identifier.
        :type id: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        '''

        # Verify the reading exists before deletion.
        self.verify(
            expression=self.reading_service.exists(id),
            error_code=READING_NOT_FOUND_ID,
            id=id,
        )

        # Delete via the service.
        self.reading_service.delete(id)
