"""I Ching Engine Embedding Events"""

# *** imports

# ** core
from typing import Dict, List, Optional

# ** app
from tiferet.events import DomainEvent
from tiferet_kb import DocumentService

from ..interfaces.embedding import EmbeddingService
from ..repos.hexagram import HEXAGRAM_CATEGORY_ID

# *** events

# ** event: embed_hexagrams
class EmbedHexagrams(DomainEvent):
    '''
    Event to generate and store embedding vectors for all hexagram sections.

    Iterates over all hexagram documents in the KB, extracts text content
    from each section (judgement, image, changing lines), generates
    embeddings via the embedding service, and stores them via the
    document service.
    '''

    # * attribute: document_service
    document_service: DocumentService

    # * attribute: embedding_service
    embedding_service: EmbeddingService

    # * init
    def __init__(self,
            document_service: DocumentService,
            embedding_service: EmbeddingService,
        ):
        '''
        Initialize the EmbedHexagrams event.

        :param document_service: The KB document service.
        :type document_service: DocumentService
        :param embedding_service: The embedding generation service.
        :type embedding_service: EmbeddingService
        '''

        # Set dependencies.
        self.document_service = document_service
        self.embedding_service = embedding_service

    # * method: execute
    def execute(self, **kwargs) -> int:
        '''
        Generate and store embeddings for all hexagram sections.

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The number of sections embedded.
        :rtype: int
        '''

        # Get the model name for storage.
        model_name = self.embedding_service.get_model_name()

        # List all hexagram document headers.
        doc_headers = self.document_service.list(category_id=HEXAGRAM_CATEGORY_ID)

        # Embed each document's sections.
        count = 0
        for header in doc_headers:

            # Load the full document with sections.
            doc = self.document_service.get(header.id)
            if doc is None or not doc.sections:
                continue

            for section in doc.sections:

                # Extract embeddable text from the section content.
                text = _extract_text(section.content)
                if not text:
                    continue

                # Prepend the section title for context.
                embed_text = f'{section.title}: {text}'

                # Generate and store the embedding.
                vector = self.embedding_service.embed(embed_text)
                self.document_service.embed_section(section.id, vector, model_name)
                count += 1

        # Return the number of sections embedded.
        return count


# ** event: search_hexagrams
class SearchHexagrams(DomainEvent):
    '''
    Event to perform semantic search over hexagram content.

    Takes a natural language query, generates a query embedding, searches
    the KB for similar hexagram sections, and returns enriched results
    with hexagram context.
    '''

    # * attribute: document_service
    document_service: DocumentService

    # * attribute: embedding_service
    embedding_service: EmbeddingService

    # * init
    def __init__(self,
            document_service: DocumentService,
            embedding_service: EmbeddingService,
        ):
        '''
        Initialize the SearchHexagrams event.

        :param document_service: The KB document service.
        :type document_service: DocumentService
        :param embedding_service: The embedding generation service.
        :type embedding_service: EmbeddingService
        '''

        # Set dependencies.
        self.document_service = document_service
        self.embedding_service = embedding_service

    # * method: execute
    @DomainEvent.parameters_required(['query'])
    def execute(self,
            query: str,
            limit: int = 5,
            **kwargs,
        ) -> List[Dict]:
        '''
        Search hexagram content by semantic similarity.

        :param query: The natural language search query.
        :type query: str
        :param limit: Maximum number of results to return.
        :type limit: int
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: A ranked list of result dicts with hexagram context.
        :rtype: List[Dict]
        '''

        # Generate the query embedding.
        query_embedding = self.embedding_service.embed(query)

        # Search the KB for similar sections within the hexagrams category.
        raw_results = self.document_service.search_similar(
            query_embedding=query_embedding,
            limit=limit,
            category_id=HEXAGRAM_CATEGORY_ID,
        )

        # Return empty if no results.
        if not raw_results:
            return []

        # Build a section lookup from all hexagram documents.
        section_lookup = _build_section_lookup(self.document_service)

        # Enrich each result with hexagram context.
        enriched = []
        for result in raw_results:
            section_id = result['section_id']
            info = section_lookup.get(section_id)
            if info is None:
                continue

            enriched.append({
                'hexagram_number': info['hexagram_number'],
                'hexagram_name': info['hexagram_name'],
                'section_title': info['section_title'],
                'content': info['content'],
                'score': result['score'],
            })

        # Return the enriched results.
        return enriched


# *** helpers

# ** helper: _extract_text
def _extract_text(content: str) -> str:
    '''
    Extract embeddable text from section content,
    stripping the @meta JSON prefix if present.

    :param content: The raw section content.
    :type content: str
    :return: The extracted text, or empty string.
    :rtype: str
    '''

    # Handle empty content.
    if not content or not content.strip():
        return ''

    # Strip @meta prefix (used by changing line sections).
    if content.startswith('@meta '):
        first_line, *rest = content.split('\n')
        return '\n'.join(rest).strip()

    # Return the content as-is.
    return content.strip()


# ** helper: _build_section_lookup
def _build_section_lookup(document_service: DocumentService) -> Dict[str, Dict]:
    '''
    Build a mapping from section_id to hexagram context info.

    :param document_service: The KB document service.
    :type document_service: DocumentService
    :return: Dict mapping section_id to context dict.
    :rtype: Dict[str, Dict]
    '''

    # List all hexagram document headers.
    doc_headers = document_service.list(category_id=HEXAGRAM_CATEGORY_ID)

    # Build the lookup by loading each document's sections.
    lookup = {}
    for header in doc_headers:
        doc = document_service.get(header.id)
        if doc is None:
            continue

        # Parse hexagram number and name from the document.
        hexagram_number = int(doc.id.replace('hexagram-', ''))
        hexagram_name = doc.title.split('. ', 1)[-1] if '. ' in doc.title else doc.title

        for section in (doc.sections or []):
            lookup[section.id] = {
                'hexagram_number': hexagram_number,
                'hexagram_name': hexagram_name,
                'section_title': section.title,
                'content': _extract_text(section.content),
            }

    # Return the completed lookup.
    return lookup
