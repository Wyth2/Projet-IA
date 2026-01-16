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
    
    # Store the user's original query, profile and found documents
    user_query: str = ""
    user_profile: Optional[Dict[str, Any]] = None
    found_documents: List[Any] = []
    
    @property
    def _llm_type(self) -> str:
        return "simple_local"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Generate a simple response based on the retrieved documents."""
        question = self.user_query.lower()
        
        # If we have documents, use them to create the response
        if self.found_documents:
            response = "Voici mes recommandations de films pour vous :\n\n"
            for i, doc in enumerate(self.found_documents[:5], 1):
                metadata = doc.metadata
                title = metadata.get('title', 'Film inconnu')
                year = metadata.get('year', 'N/A')
                rating = metadata.get('rating', 'N/A')
                director = metadata.get('director', 'N/A')
                
                # Extract description from content
                content = doc.page_content
                desc_start = content.find("Description: ")
                if desc_start != -1:
                    desc = content[desc_start + 13:].split("\n")[0]
                else:
                    desc = content[:500]
                
                response += f"{i}. **{title}** ({year}) - Note: {rating}/10\n"
                response += f"   Réalisé par {director}.\n"
                response += f"   {desc}\n\n"
            
            return response.strip()
        
        # Fallback if no documents
        return "Désolé, je n'ai pas trouvé de films correspondants à votre recherche."


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
        self.recommended_movies = set()  # Track recommended movie IDs
        
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
            # Extract genre keywords from query
            genre_keywords = self._extract_genre_from_query(query)
            
            # Get relevant documents - request more to filter out already recommended
            docs = self.vectorstore.similarity_search(query, k=settings.top_k_results * 10)
            
            # Filter by genre if specified, and exclude already recommended
            filtered_docs = []
            for doc in docs:
                movie_id = doc.metadata.get("id")
                if movie_id in self.recommended_movies:
                    continue
                    
                # If genre specified, check if movie matches
                if genre_keywords:
                    movie_genres = doc.metadata.get("genre", "[]")
                    import json
                    try:
                        genres_list = json.loads(movie_genres) if isinstance(movie_genres, str) else movie_genres
                        genres_lower = [g.lower() for g in genres_list]
                        
                        # Check if any requested genre matches movie genres
                        if not any(keyword in genre for genre in genres_lower for keyword in genre_keywords):
                            continue
                    except:
                        pass
                
                filtered_docs.append(doc)
                self.recommended_movies.add(movie_id)
                if len(filtered_docs) >= settings.top_k_results:
                    break
            
            # Pass documents to LLM
            self.llm.found_documents = filtered_docs
            
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
                    for doc in filtered_docs
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
        
        # Extract genre keywords from query
        genre_keywords = self._extract_genre_from_query(query)
        
        # Request more results to account for potential duplicates and already recommended
        results = self.vectorstore.similarity_search(query, k=k*10)
        
        # Deduplicate by movie ID, filter by genre, and exclude already recommended
        seen_ids = set()
        unique_results = []
        
        for doc in results:
            movie_id = doc.metadata.get("id")
            if movie_id in seen_ids or movie_id in self.recommended_movies:
                continue
            
            # If genre specified, check if movie matches
            if genre_keywords:
                movie_genres = doc.metadata.get("genre", "[]")
                import json
                try:
                    genres_list = json.loads(movie_genres) if isinstance(movie_genres, str) else movie_genres
                    genres_lower = [g.lower() for g in genres_list]
                    
                    # Check if any requested genre matches movie genres
                    if not any(keyword in genre for genre in genres_lower for keyword in genre_keywords):
                        continue
                except:
                    pass
            
            seen_ids.add(movie_id)
            self.recommended_movies.add(movie_id)
            unique_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
            
            if len(unique_results) >= k:
                break
        
        return unique_results
    
    def _extract_genre_from_query(self, query: str) -> List[str]:
        """Extract genre keywords from user query."""
        query_lower = query.lower()
        genre_map = {
            "action": ["action"],
            "aventure": ["adventure", "aventure"],
            "comédie": ["comedy", "comedie", "comédie"],
            "drame": ["drama", "drame"],
            "horreur": ["horror", "horreur", "épouvante"],
            "science-fiction": ["sci-fi", "science fiction", "science-fiction", "sf"],
            "thriller": ["thriller", "suspense"],
            "romance": ["romance", "romantique"],
            "fantastique": ["fantasy", "fantastique"],
            "animation": ["animation", "animé"],
            "crime": ["crime", "policier"],
            "guerre": ["war", "guerre"],
            "western": ["western"]
        }
        
        found_genres = []
        for genre, keywords in genre_map.items():
            if any(keyword in query_lower for keyword in keywords):
                found_genres.append(genre)
        
        return found_genres
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.chat_history = []
        self.recommended_movies.clear()
        print("Conversation history and recommended movies cleared")
    
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
        
        # Extract genre keywords from query
        genre_keywords = self._extract_genre_from_query(query)
        
        # Search for similar movies - request more to account for duplicates and already recommended
        results = self.vectorstore.similarity_search(query, k=k*10)
        
        # Deduplicate by movie ID, filter by genre, and exclude already recommended
        seen_ids = set()
        suggestions = []
        
        for doc in results:
            metadata = doc.metadata
            movie_id = metadata.get("id")
            
            # Skip if we've already added this movie or it was recommended before
            if movie_id in seen_ids or movie_id in self.recommended_movies:
                continue
            
            # If genre specified, check if movie matches
            if genre_keywords:
                movie_genres = metadata.get("genre", "[]")
                import json
                try:
                    genres_list = json.loads(movie_genres) if isinstance(movie_genres, str) else movie_genres
                    genres_lower = [g.lower() for g in genres_list]
                    
                    # Check if any requested genre matches movie genres
                    if not any(keyword in genre for genre in genres_lower for keyword in genre_keywords):
                        continue
                except:
                    pass
            
            seen_ids.add(movie_id)
            self.recommended_movies.add(movie_id)
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
