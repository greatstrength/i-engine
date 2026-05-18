"""I Ching Engine Reading Repository"""

# *** imports

# ** core
import json
from typing import Dict, List, Optional

# ** app
from tiferet_kb import (
    CategoryService,
    DocumentService,
    CategoryAggregate,
    DocumentAggregate,
    DocumentSectionAggregate,
)

from ..interfaces.reading import ReadingService
from ..domain.reading import Reading, ResultLine, HexagramResult

# *** constants

# ** constant: reading_category_id
READING_CATEGORY_ID = 'readings'

# ** constant: reading_category_name
READING_CATEGORY_NAME = 'I Ching Readings'

# *** repos

# ** repo: reading_kb_repository
class ReadingKBRepository(ReadingService):
    '''
    Knowledge base-backed repository for I Ching readings.

    Stores each reading as a tiferet-kb Document with sections for
    metadata, result lines, and hexagram references.
    '''

    # * attribute: document_service
    document_service: DocumentService

    # * attribute: category_service
    category_service: CategoryService

    # * init
    def __init__(self,
            document_service: DocumentService,
            category_service: CategoryService,
        ):
        '''
        Initialize the reading repository.

        :param document_service: The KB document service.
        :type document_service: DocumentService
        :param category_service: The KB category service.
        :type category_service: CategoryService
        '''

        # Set dependencies.
        self.document_service = document_service
        self.category_service = category_service

        # Ensure the readings category exists.
        if not self.category_service.exists(READING_CATEGORY_ID):
            category = CategoryAggregate(
                id=READING_CATEGORY_ID,
                name=READING_CATEGORY_NAME,
                icon='☷',
            )
            self.category_service.save(category)

    # * method: exists
    def exists(self, id: str) -> bool:
        '''
        Check if a reading exists by ID.

        :param id: The reading identifier.
        :type id: str
        :return: True if the reading exists.
        :rtype: bool
        '''

        # Check via the document service.
        return self.document_service.exists(id)

    # * method: get
    def get(self, id: str) -> Optional[Reading]:
        '''
        Retrieve a reading by ID.

        :param id: The reading identifier.
        :type id: str
        :return: The reading domain object, or None.
        :rtype: Reading | None
        '''

        # Fetch the KB document.
        doc = self.document_service.get(id)

        # Return None if the document does not exist.
        if doc is None:
            return None

        # Map the KB document to a Reading domain object.
        return self._to_reading(doc)

    # * method: list
    def list(self,
            reading_type: Optional[str] = None,
            frequency: Optional[str] = None,
            date: Optional[str] = None,
        ) -> List[Reading]:
        '''
        List readings with optional filters.

        :param reading_type: Optional reading type filter.
        :type reading_type: str | None
        :param frequency: Optional frequency filter.
        :type frequency: str | None
        :param date: Optional date filter (ISO format).
        :type date: str | None
        :return: A list of reading domain objects.
        :rtype: List[Reading]
        '''

        # Retrieve all document headers in the readings category.
        doc_headers = self.document_service.list(category_id=READING_CATEGORY_ID)

        # Load full documents (with sections) for each header.
        readings = []
        for header in doc_headers:
            full_doc = self.document_service.get(header.id)
            if full_doc is not None:
                readings.append(self._to_reading(full_doc))

        # Apply filters.
        if reading_type is not None:
            readings = [r for r in readings if r.type == reading_type]
        if frequency is not None:
            readings = [r for r in readings if r.frequency == frequency]
        if date is not None:
            readings = [r for r in readings if r.date == date]

        # Return the filtered list.
        return readings

    # * method: save
    def save(self, reading: Reading) -> None:
        '''
        Persist a reading as a KB document with sections.

        :param reading: The reading to save.
        :type reading: Reading
        '''

        # Build the document.
        doc = DocumentAggregate(
            id=reading.id,
            title=reading.name,
            category_id=READING_CATEGORY_ID,
            status='published',
        )

        # Save the document header.
        self.document_service.save(doc)

        # Track section position.
        position = 0

        # Metadata section.
        metadata = json.dumps({
            'dimension': reading.dimension,
            'frequency': reading.frequency,
            'type': reading.type,
            'date': reading.date,
            'created_at': reading.created_at,
        })
        section = DocumentSectionAggregate(
            document_id=reading.id,
            title='Metadata',
            content_type='text',
            content=metadata,
            position=position,
        )
        self.document_service.save_section(section)
        position += 1

        # Result line sections.
        for line in reading.result_lines:
            line_data = json.dumps({
                'position': line.position,
                'heaven_line': line.heaven_line,
                'man_line': line.man_line,
                'earth_line': line.earth_line,
                'line_value': line.line_value,
            })
            section = DocumentSectionAggregate(
                document_id=reading.id,
                title=f'Line {line.position}',
                content_type='text',
                content=line_data,
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

        # Current/previous hexagram section (optional).
        if reading.current_or_previous:
            hex_data = json.dumps({
                'name': reading.current_or_previous.name,
                'number': reading.current_or_previous.number,
            })
            section = DocumentSectionAggregate(
                document_id=reading.id,
                title='Current Hexagram',
                content_type='text',
                content=hex_data,
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

        # Next hexagram section (optional).
        if reading.next:
            hex_data = json.dumps({
                'name': reading.next.name,
                'number': reading.next.number,
            })
            section = DocumentSectionAggregate(
                document_id=reading.id,
                title='Next Hexagram',
                content_type='text',
                content=hex_data,
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

    # * method: delete
    def delete(self, id: str) -> None:
        '''
        Delete a reading by ID. This operation is idempotent.

        :param id: The reading identifier.
        :type id: str
        '''

        # Delegate to the KB document delete.
        self.document_service.delete(id)

    # * method: _to_reading
    def _to_reading(self, doc) -> Reading:
        '''
        Map a KB document (with sections) to a Reading domain object.

        :param doc: The KB document aggregate.
        :return: The reading domain object.
        :rtype: Reading
        '''

        # Retrieve sections.
        sections = doc.sections if hasattr(doc, 'sections') and doc.sections else []

        # Parse sections into metadata, result lines, and hexagram references.
        metadata = {}
        result_lines = []
        current_or_previous = None
        next_hex = None

        for section in sections:
            if section.title == 'Metadata':
                metadata = json.loads(section.content) if section.content else {}
            elif section.title.startswith('Line '):
                line_data = json.loads(section.content) if section.content else {}
                if line_data:
                    result_lines.append(ResultLine(**line_data))
            elif section.title == 'Current Hexagram':
                hex_data = json.loads(section.content) if section.content else {}
                if hex_data:
                    current_or_previous = HexagramResult(**hex_data)
            elif section.title == 'Next Hexagram':
                hex_data = json.loads(section.content) if section.content else {}
                if hex_data:
                    next_hex = HexagramResult(**hex_data)

        # Sort result lines by position.
        result_lines.sort(key=lambda l: l.position)

        # Construct and return the Reading.
        return Reading(
            id=doc.id,
            name=doc.title,
            dimension=metadata.get('dimension', '2'),
            frequency=metadata.get('frequency', 'daily'),
            type=metadata.get('type', 'general'),
            date=metadata.get('date', ''),
            created_at=metadata.get('created_at', ''),
            result_lines=result_lines,
            current_or_previous=current_or_previous,
            next=next_hex,
        )
