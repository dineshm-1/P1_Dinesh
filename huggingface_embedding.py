from chromadb.api.types import (
    Documents,
    EmbeddingFunction,
    Embeddings,
)

class HuggingFaceEmbeddingInference(EmbeddingFunction[Documents]):
    """
    This class is a modification of ChromaDB's HuggingFaceEmbeddingServer class. It has been modified to accept API authorization key and to pass it in the request header. Moreover, it adds a simple error handling.
    """

    def __init__(self, url: str, key: str):
        """
        Initialize the HuggingFaceEmbeddingInference.

        Args:
            url (str): The URL of the HuggingFace Embedding Server.
            key (str): The authorization key for the HuggingFace Embedding Server.
        """
        try:
            import requests
        except ImportError:
            raise ValueError(
                "The requests python package is not installed. Please install it with `pip install requests`"
            )
        self._api_url = f"{url}"
        self._api_key = f"{key}"
        self._session = requests.Session()

    def __call__(self, input: Documents) -> Embeddings:
        """
        Get the embeddings for a list of texts.

        Args:
            texts (Documents): A list of texts to get embeddings for.

        Returns:
            Embeddings: The embeddings for the texts.

        Example:
            >>> hugging_face = HuggingFaceEmbeddingInference(url="http://localhost:8080/embed", key="api_key")
            >>> texts = ["Hello, world!", "How are you?"]
            >>> embeddings = hugging_face(texts)
        """
        # Call HuggingFace Embedding Inference Endpoint API for each document
        response = self._session.post(  # type: ignore
            self._api_url, json={"inputs": input, "parameters": {"wait_for_model": "true"}}, headers={"authorization": f"Bearer {self._api_key}"}
        ).json()

        # If Endpoint returns an error, don't return the response but raise Exception
        if type(response) is dict and 'error' in response.keys():
            raise ValueError("There is an error, please try again in a few moments", response)
        else:
            return response