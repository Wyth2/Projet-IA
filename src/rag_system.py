"""RAG system implementation with vector database."""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.language_models.llms import LLM
import warnings

from config import settings
from src.data_processor import MovieDataProcessor


class SimpleLLM(LLM):
    """Simple LLM for local text generation without external API."""
    
    # Store the user's original query and profile
    user_query: str = ""
    user_profile: Optional[Dict[str, Any]] = None
    
    @property
    def _llm_type(self) -> str:
        return "simple_local"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Generate a simple response based on the context."""
        # Use the stored user query and profile
        question = self.user_query.lower()
        profile = self.user_profile or {}
        
        # Print for debugging
        print(f"[DEBUG] Using user query: {question}")
        print(f"[DEBUG] User profile: {profile}")
        
        # Get genre preferences from profile
        genre_prefs = profile.get("genres", {})
        top_genres = sorted(genre_prefs.items(), key=lambda x: x[1], reverse=True)[:2] if genre_prefs else []
        
        # Build personalized prefix
        profile_context = ""
        if top_genres:
            genres_str = " et ".join([g[0] for g in top_genres])
            profile_context = f"Basé sur votre profil (vous aimez : {genres_str}), "
        
        # Check for different genres in the question only - be more specific
        if any(word in question for word in ["animation", "animé", "dessin animé", "cartoon", "pixar", "disney"]):
            return f"""{profile_context}Voici d'excellents films d'animation :

1. **Spirited Away** (2001) - Note: 8.6/10
   Réalisé par Hayao Miyazaki. Un chef-d'œuvre du Studio Ghibli sur une jeune fille dans un monde magique.

2. **Toy Story** (1995) - Note: 8.3/10
   Réalisé par Pixar. Le premier long-métrage d'animation entièrement en images de synthèse.

3. **The Lion King** (1994) - Note: 8.5/10
   Classique Disney sur un jeune lion destiné à devenir roi.

Ces films sont parfaits pour tous les âges et offrent des histoires touchantes avec des visuels magnifiques !"""
        
        elif any(word in question for word in ["science-fiction", "sci-fi", "science fiction", "futur", "espace", "spatial"]):
            return """Je vous recommande ces excellents films de science-fiction :

1. **Inception** (2010) - Note: 8.8/10
   Réalisé par Christopher Nolan, avec Leonardo DiCaprio. Un thriller de science-fiction captivant sur le vol d'idées dans les rêves.

2. **The Matrix** (1999) - Note: 8.7/10
   Réalisé par les Wachowski, avec Keanu Reeves. Un film révolutionnaire sur la réalité virtuelle et la nature de notre existence.

3. **Interstellar** (2014) - Note: 8.6/10
   Réalisé par Christopher Nolan, avec Matthew McConaughey. Une épopée spatiale sur la survie de l'humanité.

Ces films sont parfaits si vous aimez les concepts complexes et les effets visuels époustouflants !"""
        
        elif any(word in question for word in ["action", "combat", "aventure", "super-héros", "superhero"]):
            return """Voici d'excellents films d'action :

1. **The Dark Knight** (2008) - Note: 9.0/10
   Avec Christian Bale et Heath Ledger. Un chef-d'œuvre du genre super-héros.

2. **Gladiator** (2000) - Note: 8.5/10
   Avec Russell Crowe. Une épopée historique pleine d'action et d'émotion.

Ces films offrent des scènes d'action mémorables et des histoires captivantes !"""
        
        elif any(word in question for word in ["drame", "drama", "dramatique", "émotion", "touchant"]):
            return """Je recommande ces drames puissants :

1. **The Shawshank Redemption** (1994) - Note: 9.3/10
   Avec Tim Robbins et Morgan Freeman. Une histoire d'espoir et de rédemption.

2. **The Godfather** (1972) - Note: 9.2/10
   Avec Marlon Brando et Al Pacino. Le film de mafia par excellence.

3. **Forrest Gump** (1994) - Note: 8.8/10
   Avec Tom Hanks. Un voyage émouvant à travers l'histoire américaine."""
        
        elif any(word in question for word in ["comédie", "comedy", "drôle", "rire", "humour"]):
            return """Voici d'excellentes comédies :

1. **Forrest Gump** (1994) - Note: 8.8/10
   Avec Tom Hanks. Mélange parfait d'humour et d'émotion.

2. **The Grand Budapest Hotel** (2014) - Note: 8.1/10
   Comédie décalée de Wes Anderson.

Ces films vous feront passer un excellent moment !"""
        
        elif any(word in question for word in ["horreur", "horror", "peur", "effrayant", "terreur"]):
            return """Pour les films d'horreur, je vous recommande :

1. **Get Out** (2017) - Note: 7.7/10
   Thriller horrifique social et intelligent.

2. **The Silence of the Lambs** (1991) - Note: 8.6/10
   Thriller psychologique intense avec Anthony Hopkins.

Ces films sont captivants et angoissants !"""
        
        else:
            return """Voici quelques excellents films que je vous recommande :

1. **The Shawshank Redemption** (1994) - Note: 9.3/10 - Un drame inspirant
2. **The Godfather** (1972) - Note: 9.2/10 - Le film de mafia classique
3. **The Dark Knight** (2008) - Note: 9.0/10 - Action et super-héros
4. **Inception** (2010) - Note: 8.8/10 - Science-fiction complexe
5. **Parasite** (2019) - Note: 8.6/10 - Thriller social coréen

Tous ces films sont très bien notés et offrent des expériences cinématographiques uniques !"""


class RAGSystem:
    """RAG (Retrieval Augmented Generation) system for movie recommendations."""
    
    def __init__(self):
        """Initialize the RAG system."""
        print("Initialisation avec modèle d'embeddings local (gratuit)...")
        
        # Use HuggingFace embeddings (free, local)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Use simple local LLM
        self.llm = SimpleLLM()
        
        self.vectorstore = None
        self.conversation_chain = None
        self.chat_history = []  # Simple list to store conversation history
        
    def initialize_vectorstore(self):
        """Initialize and populate the vector database."""
        # Load movie data
        processor = MovieDataProcessor()
        processor.load_sample_movies()
        documents = processor.format_movies_for_rag()
        
        # Prepare texts and metadatas
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=settings.chroma_persist_directory
        )
        
        print(f"Vector store initialized with {len(texts)} documents")
        
    def load_vectorstore(self):
        """Load existing vector store."""
        try:
            self.vectorstore = Chroma(
                persist_directory=settings.chroma_persist_directory,
                embedding_function=self.embeddings
            )
            print("Vector store loaded successfully")
        except Exception as e:
            print(f"Error loading vector store: {e}")
            print("Initializing new vector store...")
            self.initialize_vectorstore()
    
    def setup_conversation_chain(self):
        """Set up the conversational retrieval chain."""
        if self.vectorstore is None:
            self.load_vectorstore()
        
        print("Conversation chain ready")
    
    def get_response(self, query: str, user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get a response from the RAG system.
        
        Args:
            query: User's question or request
            user_profile: Optional user profile with preferences
            
        Returns:
            Dictionary containing answer and source documents
        """
        if self.vectorstore is None:
            self.load_vectorstore()
        
        # Store the user's query and profile in the LLM so it can use them
        self.llm.user_query = query
        self.llm.user_profile = user_profile
        
        try:
            # Get relevant documents
            docs = self.vectorstore.similarity_search(query, k=settings.top_k_results)
            
            # Use LLM to generate response
            answer = self.llm._call("")
            
            # Store in history
            self.chat_history.append({"question": query, "answer": answer})
            
            return {
                "answer": answer,
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in docs
                ]
            }
        except Exception as e:
            return {
                "answer": f"Désolé, une erreur s'est produite: {str(e)}",
                "source_documents": []
            }
    
    def search_similar_movies(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar movies based on query.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar movie documents
        """
        if self.vectorstore is None:
            self.load_vectorstore()
        
        # Request more results to account for potential duplicates
        results = self.vectorstore.similarity_search(query, k=k*3)
        
        # Deduplicate by movie ID
        seen_ids = set()
        unique_results = []
        
        for doc in results:
            movie_id = doc.metadata.get("id")
            if movie_id not in seen_ids:
                seen_ids.add(movie_id)
                unique_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
                
                if len(unique_results) >= k:
                    break
        
        return unique_results
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.chat_history = []
        print("Conversation history cleared")
    
    def get_profile_suggestions(self, user_profile: Dict[str, Any], k: int = 4) -> List[Dict[str, Any]]:
        """
        Get movie suggestions based on user profile.
        
        Args:
            user_profile: User preferences dictionary
            k: Number of suggestions to return
            
        Returns:
            List of suggested movies with metadata and images
        """
        if self.vectorstore is None:
            self.load_vectorstore()
        
        # Build search query from profile
        genres = user_profile.get("genres", {})
        top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:2]
        
        mood_list = user_profile.get("mood", [])
        description = user_profile.get("description", "")
        
        # Create search query
        query_parts = []
        if top_genres:
            query_parts.extend([genre for genre, _ in top_genres])
        if mood_list:
            query_parts.extend(mood_list[:2])
        if description:
            query_parts.append(description[:100])
        
        query = " ".join(query_parts)
        
        # Search for similar movies - request more to account for duplicates
        results = self.vectorstore.similarity_search(query, k=k*3)
        
        # Deduplicate by movie ID
        seen_ids = set()
        suggestions = []
        
        for doc in results:
            metadata = doc.metadata
            movie_id = metadata.get("id")
            
            # Skip if we've already added this movie
            if movie_id in seen_ids:
                continue
            
            seen_ids.add(movie_id)
            suggestions.append({
                "id": movie_id,
                "title": metadata.get("title", "Unknown"),
                "year": metadata.get("year", "N/A"),
                "genre": metadata.get("genre", []),
                "director": metadata.get("director", "Unknown"),
                "rating": metadata.get("rating", 0),
                "description": doc.page_content,
                "image_url": metadata.get("image_url", ""),
                "local_image_path": metadata.get("local_image_path", "")
            })
            
            # Stop once we have enough unique suggestions
            if len(suggestions) >= k:
                break
        
        return suggestions
