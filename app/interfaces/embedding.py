"""I Ching Engine Interfaces Embedding"""

# *** imports

# ** core
from abc import abstractmethod
from typing import List

# ** app
from tiferet.interfaces import Service

# *** interfaces

# ** interface: embedding_service
class EmbeddingService(Service):
    '''
    Service interface for generating text embedding vectors.
    '''

    # * method: embed
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        '''
        Generate an embedding vector for a single text string.

        :param text: The text to embed.
        :type text: str
        :return: The embedding vector.
        :rtype: List[float]
        '''
        raise NotImplementedError()

    # * method: embed_batch
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        '''
        Generate embedding vectors for a batch of text strings.

        :param texts: The texts to embed.
        :type texts: List[str]
        :return: A list of embedding vectors.
        :rtype: List[List[float]]
        '''
        raise NotImplementedError()

    # * method: get_model_name
    @abstractmethod
    def get_model_name(self) -> str:
        '''
        Return the name of the embedding model.

        :return: The model name string.
        :rtype: str
        '''
        raise NotImplementedError()
