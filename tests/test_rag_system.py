"""Tests unitaires pour le système RAG."""
import unittest
from unittest.mock import Mock, patch
from src.data_processor import MovieDataProcessor
from src.rag_system import RAGSystem


class TestMovieDataProcessor(unittest.TestCase):
    """Tests pour le processeur de données de films."""
    
    def setUp(self):
        """Initialisation avant chaque test."""
        self.processor = MovieDataProcessor()
    
    def test_load_sample_movies(self):
        """Test du chargement des films d'exemple."""
        movies = self.processor.load_sample_movies()
        
        self.assertIsInstance(movies, list)
        self.assertGreater(len(movies), 0)
        self.assertIn("title", movies[0])
        self.assertIn("description", movies[0])
    
    def test_get_movie_text(self):
        """Test de la conversion d'un film en texte."""
        movie = {
            "title": "Test Movie",
            "year": 2020,
            "genre": ["Action"],
            "director": "Test Director",
            "description": "Test description",
            "rating": 8.0,
            "actors": ["Actor 1", "Actor 2"]
        }
        
        text = self.processor.get_movie_text(movie)
        
        self.assertIn("Test Movie", text)
        self.assertIn("2020", text)
        self.assertIn("Action", text)
    
    def test_format_movies_for_rag(self):
        """Test du formatage des films pour RAG."""
        self.processor.load_sample_movies()
        documents = self.processor.format_movies_for_rag()
        
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)
        self.assertIn("content", documents[0])
        self.assertIn("metadata", documents[0])


class TestRAGSystem(unittest.TestCase):
    """Tests pour le système RAG."""
    
    @patch('src.rag_system.OpenAIEmbeddings')
    @patch('src.rag_system.ChatOpenAI')
    def setUp(self, mock_chat, mock_embeddings):
        """Initialisation avant chaque test."""
        self.rag_system = RAGSystem()
    
    def test_initialization(self):
        """Test de l'initialisation du système RAG."""
        self.assertIsNotNone(self.rag_system.embeddings)
        self.assertIsNotNone(self.rag_system.llm)
        self.assertIsNotNone(self.rag_system.memory)


if __name__ == "__main__":
    unittest.main()
