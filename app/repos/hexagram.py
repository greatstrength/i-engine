"""I Ching Engine Hexagram Repository"""

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

from ..interfaces.hexagram import HexagramService
from ..domain.hexagram import Hexagram, ChangingLine

# *** constants

# ** constant: hexagram_category_id
HEXAGRAM_CATEGORY_ID = 'hexagrams'

# ** constant: hexagram_category_name
HEXAGRAM_CATEGORY_NAME = 'I Ching Hexagrams'

# *** repos

# ** repo: hexagram_kb_repository
class HexagramKBRepository(HexagramService):
    '''
    Knowledge base-backed repository for I Ching hexagrams.

    Stores each hexagram as a tiferet-kb Document with sections for
    judgement, image, and each changing line. Supports embedding-based
    semantic search.
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
        Initialize the hexagram repository.

        :param document_service: The KB document service.
        :type document_service: DocumentService
        :param category_service: The KB category service.
        :type category_service: CategoryService
        '''

        # Set dependencies.
        self.document_service = document_service
        self.category_service = category_service

        # Ensure the hexagrams category exists.
        if not self.category_service.exists(HEXAGRAM_CATEGORY_ID):
            category = CategoryAggregate(
                id=HEXAGRAM_CATEGORY_ID,
                name=HEXAGRAM_CATEGORY_NAME,
                icon='☰',
            )
            self.category_service.save(category)

    # * method: exists
    def exists(self, number: int) -> bool:
        '''
        Check if a hexagram exists by its Wilhelm number.

        :param number: The hexagram number (1 to 64).
        :type number: int
        :return: True if the hexagram exists.
        :rtype: bool
        '''

        # Use the hexagram number as the document ID.
        doc_id = self._doc_id(number)

        # Check via the document service.
        return self.document_service.exists(doc_id)

    # * method: get
    def get(self, number: int) -> Optional[Hexagram]:
        '''
        Retrieve a hexagram by its Wilhelm number.

        :param number: The hexagram number (1 to 64).
        :type number: int
        :return: The hexagram domain object, or None.
        :rtype: Hexagram | None
        '''

        # Fetch the KB document.
        doc_id = self._doc_id(number)
        doc = self.document_service.get(doc_id)

        # Return None if the document does not exist.
        if doc is None:
            return None

        # Map the KB document to a Hexagram domain object.
        return self._to_hexagram(doc)

    # * method: list
    def list(self) -> List[Hexagram]:
        '''
        List all hexagrams.

        :return: A list of hexagram domain objects.
        :rtype: List[Hexagram]
        '''

        # Retrieve all documents in the hexagrams category.
        docs = self.document_service.list(category_id=HEXAGRAM_CATEGORY_ID)

        # Map each document to a Hexagram.
        return [self._to_hexagram(doc) for doc in docs]

    # * method: save
    def save(self, hexagram: Hexagram) -> None:
        '''
        Persist a hexagram as a KB document with sections.

        :param hexagram: The hexagram to save.
        :type hexagram: Hexagram
        '''

        # Build the document.
        doc_id = self._doc_id(hexagram.number)
        doc = DocumentAggregate(
            id=doc_id,
            title=f'{hexagram.number}. {hexagram.name}',
            category_id=HEXAGRAM_CATEGORY_ID,
            status='published',
        )

        # Save the document header.
        self.document_service.save(doc)

        # Build sections: judgement, image, then changing lines.
        position = 0

        # Judgement section.
        if hexagram.judgement:
            section = DocumentSectionAggregate(
                document_id=doc_id,
                title='Judgement',
                content_type='text',
                content='\n'.join(hexagram.judgement),
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

        # Image section.
        if hexagram.image:
            section = DocumentSectionAggregate(
                document_id=doc_id,
                title='Image',
                content_type='text',
                content='\n'.join(hexagram.image),
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

        # Changing line sections.
        for line in hexagram.changing_lines:
            section = DocumentSectionAggregate(
                document_id=doc_id,
                title=f'Line {line.line_number}',
                content_type='text',
                content=self._serialize_line_content(line),
                position=position,
            )
            self.document_service.save_section(section)
            position += 1

    # * method: search
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
        :return: A ranked list of dicts with section_id, document_id, and score.
        :rtype: List[Dict]
        '''

        # Delegate to the KB search.
        return self.document_service.search_similar(
            query_embedding=query_embedding,
            limit=limit,
            category_id=HEXAGRAM_CATEGORY_ID,
        )

    # * method: _doc_id (static)
    @staticmethod
    def _doc_id(number: int) -> str:
        '''
        Derive a deterministic document ID from the hexagram number.

        :param number: The hexagram number.
        :type number: int
        :return: The document ID string.
        :rtype: str
        '''
        return f'hexagram-{number:02d}'

    # * method: _to_hexagram
    def _to_hexagram(self, doc) -> Hexagram:
        '''
        Map a KB document (with sections) to a Hexagram domain object.

        :param doc: The KB document aggregate.
        :return: The hexagram domain object.
        :rtype: Hexagram
        '''

        # Parse the hexagram number from the document ID.
        number = int(doc.id.replace('hexagram-', ''))

        # Extract the name from the title (strip the "N. " prefix).
        name = doc.title.split('. ', 1)[-1] if '. ' in doc.title else doc.title

        # Retrieve sections.
        sections = doc.sections if hasattr(doc, 'sections') and doc.sections else []

        # Parse sections into judgement, image, and changing lines.
        judgement = []
        image = []
        changing_lines = []

        for section in sections:
            if section.title == 'Judgement':
                judgement = section.content.split('\n') if section.content else []
            elif section.title == 'Image':
                image = section.content.split('\n') if section.content else []
            elif section.title.startswith('Line '):
                line_num = int(section.title.split(' ')[1])
                line_data = self._deserialize_line_content(section.content)
                changing_lines.append(ChangingLine(
                    text=line_data['text'],
                    yarrow_value=line_data['yarrow_value'],
                    line_number=line_num,
                    type=line_data['type'],
                ))

        # Construct and return the Hexagram.
        return Hexagram(
            number=number,
            name=name,
            judgement=judgement,
            image=image,
            changing_lines=changing_lines,
        )

    # * method: _serialize_line_content (static)
    @staticmethod
    def _serialize_line_content(line: ChangingLine) -> str:
        '''
        Serialize changing line metadata and text into a section content string.

        :param line: The changing line to serialize.
        :type line: ChangingLine
        :return: The serialized section content.
        :rtype: str
        '''

        # Build the metadata header.
        metadata = json.dumps({
            'yarrow_value': line.yarrow_value,
            'type': line.type,
        })

        # Return the metadata header plus the body text.
        body = '\n'.join(line.text or [])
        return f'@meta {metadata}\n{body}' if body else f'@meta {metadata}'

    # * method: _deserialize_line_content (static)
    @staticmethod
    def _deserialize_line_content(content: str) -> Dict:
        '''
        Deserialize section content into changing line metadata and text.

        Supports the current ``@meta {json}`` format and a plain-text fallback.

        :param content: The raw section content.
        :type content: str
        :return: Dict with ``text``, ``yarrow_value``, and ``type``.
        :rtype: Dict
        '''

        # Handle empty content.
        if not content:
            return {
                'text': [],
                'yarrow_value': 9,
                'type': None,
            }

        # Parse the metadata-prefixed format when present.
        if content.startswith('@meta '):
            first_line, *rest = content.split('\n')
            metadata = json.loads(first_line.replace('@meta ', '', 1))
            return {
                'text': rest,
                'yarrow_value': metadata.get('yarrow_value', 9),
                'type': metadata.get('type'),
            }

        # Fall back to legacy plain text content.
        return {
            'text': content.split('\n'),
            'yarrow_value': 9,
            'type': None,
        }
