"""I Ching Engine Embedding Utility"""

# *** imports

# ** core
from typing import List

# ** app
from ..interfaces.embedding import EmbeddingService

# *** utils

# ** util: sentence_transformer_embedder
class SentenceTransformerEmbedder(EmbeddingService):
    '''
    Embedding utility using sentence-transformers for local vector generation.

    Lazy-loads the model on first embed call to avoid import overhead
    when the utility is instantiated but not used.
    '''

    # * attribute: _model_name
    _model_name: str

    # * attribute: _model
    _model: object

    # * init
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        '''
        Initialize the embedder.

        :param model_name: The sentence-transformers model to use.
        :type model_name: str
        '''

        # Store the model name; defer model loading.
        self._model_name = model_name
        self._model = None

    # * method: embed
    def embed(self, text: str) -> List[float]:
        '''
        Generate an embedding vector for a single text string.

        :param text: The text to embed.
        :type text: str
        :return: The embedding vector.
        :rtype: List[float]
        '''

        # Ensure the model is loaded.
        self._load_model()

        # Encode and return as a plain list.
        return self._model.encode(text).tolist()

    # * method: embed_batch
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        '''
        Generate embedding vectors for a batch of text strings.

        :param texts: The texts to embed.
        :type texts: List[str]
        :return: A list of embedding vectors.
        :rtype: List[List[float]]
        '''

        # Ensure the model is loaded.
        self._load_model()

        # Encode the batch and return as lists.
        return self._model.encode(texts).tolist()

    # * method: get_model_name
    def get_model_name(self) -> str:
        '''
        Return the name of the embedding model.

        :return: The model name string.
        :rtype: str
        '''

        return self._model_name

    # * method: _load_model
    def _load_model(self) -> None:
        '''
        Lazy-load the sentence-transformers model on first use.
        '''

        # Skip if already loaded.
        if self._model is not None:
            return

        # Import and load the model.
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)
