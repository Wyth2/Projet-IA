"""Script to initialize the vector database with movie data."""
from src.rag_system import RAGSystem
from config import settings
import os


def main():
    """Initialize the vector database."""
    print("=" * 50)
    print("Initialisation de la Base de Données Vectorielle")
    print("=" * 50)
    
    # Using local models (no API key required)
    print(f"\n✓ Utilisation de modèles locaux (gratuit)")
    print(f"✓ Modèle d'embeddings: {settings.embedding_model}")
    print(f"✓ Répertoire de persistance: {settings.chroma_persist_directory}")
    
    # Create persist directory if it doesn't exist
    os.makedirs(settings.chroma_persist_directory, exist_ok=True)
    
    # Initialize RAG system
    print("\n📚 Initialisation du système RAG...")
    rag_system = RAGSystem()
    
    # Initialize vector store
    print("\n🔄 Chargement et indexation des films...")
    rag_system.initialize_vectorstore()
    
    # Test the system
    print("\n🧪 Test du système...")
    test_query = "films de science-fiction"
    results = rag_system.search_similar_movies(test_query, k=3)
    
    print(f"\nRecherche test: '{test_query}'")
    print(f"Résultats trouvés: {len(results)}")
    
    for i, result in enumerate(results, 1):
        title = result["metadata"].get("title", "N/A")
        print(f"  {i}. {title}")
    
    print("\n" + "=" * 50)
    print("✅ Initialisation terminée avec succès!")
    print("=" * 50)
    print("\nVous pouvez maintenant lancer:")
    print("  1. L'API: python api.py")
    print("  2. L'interface: streamlit run app.py")


if __name__ == "__main__":
    main()
