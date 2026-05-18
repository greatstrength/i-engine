"""I Ching Engine KB Management Events"""

# *** imports

# ** core
from typing import Any

# ** infra
from tiferet.utils import Yaml

# ** app
from tiferet.events import DomainEvent

from ..domain.hexagram import Hexagram, ChangingLine
from ..domain.constants import KB_INGEST_FAILED_ID
from ..interfaces.hexagram import HexagramService

# *** events

# ** event: ingest_hexagram_data
class IngestHexagramData(DomainEvent):
    '''
    Event to ingest hexagram seed data from a YAML file into the knowledge base.

    Reads the seed YAML, constructs Hexagram domain objects, and persists them
    via the hexagram service.
    '''

    # * attribute: hexagram_service
    hexagram_service: HexagramService

    # * init
    def __init__(self, hexagram_service: HexagramService):
        '''
        Initialize the IngestHexagramData event.

        :param hexagram_service: The hexagram service for persistence.
        :type hexagram_service: HexagramService
        '''

        # Set the hexagram service dependency.
        self.hexagram_service = hexagram_service

    # * method: execute
    @DomainEvent.parameters_required(['seed_file'])
    def execute(self, seed_file: str, **kwargs) -> int:
        '''
        Ingest hexagram data from a YAML seed file.

        :param seed_file: Path to the hexagrams YAML seed file.
        :type seed_file: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The number of hexagrams ingested.
        :rtype: int
        '''

        # Load the seed YAML data.
        data = Yaml(path=seed_file, mode='r').load()

        # Verify data was loaded.
        self.verify(
            expression=data is not None and len(data) > 0,
            error_code=KB_INGEST_FAILED_ID,
            seed_file=seed_file,
        )

        # Ingest each hexagram.
        count = 0
        for number_str, hex_data in data.items():
            number = int(number_str)

            # Build changing lines.
            changing_lines = []
            for line_data in (hex_data.get('changing_lines') or []):
                changing_lines.append(ChangingLine(
                    text=line_data.get('text', []),
                    yarrow_value=line_data.get('yarrow_value', 9),
                    line_number=line_data.get('line_number', 1),
                    type=line_data.get('type'),
                ))

            # Build the hexagram.
            hexagram = Hexagram(
                number=number,
                name=hex_data.get('name', ''),
                secondary_names=hex_data.get('secondary_names'),
                judgement=hex_data.get('judgement', []),
                image=hex_data.get('image', []),
                changing_lines=changing_lines,
            )

            # Save via the service.
            self.hexagram_service.save(hexagram)
            count += 1

        # Return the count of ingested hexagrams.
        return count
