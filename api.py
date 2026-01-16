"""FastAPI backend for the AI Agent."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

from config import settings
from src.rag_system import RAGSystem

# Initialize FastAPI app
app = FastAPI(
    title="Agent Intelligent Sémantique et Génératif",
    description="API pour recommandations de films avec RAG",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = RAGSystem()


# Pydantic models
class QueryRequest(BaseModel):
    """Request model for queries."""
    query: str
    k: Optional[int] = 5


class ChatRequest(BaseModel):
    """Request model for chat."""
    message: str
    user_profile: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response model for chat."""
    answer: str
    source_documents: List[Dict[str, Any]]


class ProfileRequest(BaseModel):
    """Request model for profile-based suggestions."""
    user_profile: Dict[str, Any]
    k: Optional[int] = 4


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup."""
    print("Initializing RAG system...")
    rag_system.load_vectorstore()
    rag_system.setup_conversation_chain()
    print("RAG system ready!")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Bienvenue sur l'API de recommandations de films!",
        "endpoints": {
            "/chat": "Envoyer un message au chatbot",
            "/search": "Rechercher des films similaires",
            "/reset": "Réinitialiser la conversation",
            "/health": "Vérifier l'état de l'API"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "vectorstore": rag_system.vectorstore is not None,
        "conversation_chain": rag_system.conversation_chain is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI agent.
    
    Args:
        request: Chat request with user message and optional profile
        
    Returns:
        Chat response with answer and sources
    """
    try:
        response = rag_system.get_response(request.message, request.user_profile)
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_movies(request: QueryRequest):
    """
    Search for similar movies.
    
    Args:
        request: Search query and number of results
        
    Returns:
        List of similar movies
    """
    try:
        results = rag_system.search_similar_movies(
            query=request.query,
            k=request.k
        )
        return {
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_conversation():
    """Reset the conversation history."""
    try:
        rag_system.reset_conversation()
        return {"message": "Conversation réinitialisée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/suggestions")
async def get_suggestions(request: ProfileRequest):
    """Get movie suggestions based on user profile."""
    try:
        suggestions = rag_system.get_profile_suggestions(request.user_profile, request.k)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/initialize")
async def initialize_database():
    """Initialize or reinitialize the vector database."""
    try:
        rag_system.initialize_vectorstore()
        rag_system.setup_conversation_chain()
        return {"message": "Base de données vectorielle initialisée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug_mode
    )
