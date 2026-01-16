"""Streamlit UI for the AI Agent."""
import streamlit as st
import requests
import os
from typing import List, Dict, Any
import json
from PIL import Image
from io import BytesIO

# Configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Agent de Recommandations de Films",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: #000000 !important;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000 !important;
    }
    .chat-message b {
        color: #000000 !important;
    }
    .user-message {
        background-color: #e3f2fd;
        color: #000000 !important;
    }
    .assistant-message {
        background-color: #f5f5f5;
        color: #000000 !important;
    }
    .source-doc {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
        font-size: 0.9em;
        color: #000000 !important;
    }
    .source-doc b {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_healthy" not in st.session_state:
    st.session_state.api_healthy = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

if "show_profile_form" not in st.session_state:
    st.session_state.show_profile_form = True


def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def send_message(message: str) -> Dict[str, Any]:
    """Send a message to the chatbot."""
    try:
        # Include user profile in the request
        payload = {
            "message": message,
            "user_profile": st.session_state.user_profile
        }
        response = requests.post(
            f"{API_URL}/chat",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "answer": f"Erreur de communication avec l'API: {str(e)}",
            "source_documents": []
        }


def search_movies(query: str, k: int = 5) -> Dict[str, Any]:
    """Search for similar movies."""
    try:
        response = requests.post(
            f"{API_URL}/search",
            json={"query": query, "k": k},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "query": query,
            "results": []
        }


def reset_conversation():
    """Reset the conversation history."""
    try:
        response = requests.post(f"{API_URL}/reset", timeout=10)
        response.raise_for_status()
        st.session_state.messages = []
        return True
    except:
        return False


# Header
st.title("🎬 Agent Intelligent de Recommandations de Films")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check API status
    if st.button("🔄 Vérifier l'API"):
        st.session_state.api_healthy = check_api_health()
    
    if st.session_state.api_healthy:
        st.success("✅ API connectée")
    else:
        st.error("❌ API non disponible")
        st.info("Lancez l'API avec: `python api.py`")
    
    st.markdown("---")
    
    # User Profile Section
    st.header("👤 Profil Utilisateur")
    if st.session_state.user_profile:
        st.success("✅ Profil configuré")
        if st.button("📝 Modifier le profil"):
            st.session_state.show_profile_form = True
            st.rerun()
    else:
        st.warning("⚠️ Aucun profil configuré")
        if st.button("📝 Créer mon profil"):
            st.session_state.show_profile_form = True
            st.rerun()
    
    st.markdown("---")
    
    # Reset conversation
    if st.button("🗑️ Réinitialiser la conversation"):
        if reset_conversation():
            st.success("Conversation réinitialisée!")
            st.rerun()
        else:
            st.error("Erreur lors de la réinitialisation")
    
    st.markdown("---")
    
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet agent utilise:
    - **RAG** (Retrieval Augmented Generation)
    - **SBERT** pour les embeddings sémantiques
    - **ChromaDB** pour la recherche vectorielle
    - **LangChain** pour l'orchestration
    
    Posez des questions sur les films ou demandez des recommandations!
    """)

# Show Profile Form if needed
if st.session_state.show_profile_form and not st.session_state.user_profile:
    st.title("👤 Création de votre Profil Cinématographique")
    st.markdown("Répondez à ces quelques questions pour personnaliser vos recommandations.")
    
    with st.form("profile_form"):
        st.subheader("📊 Préférences par Genre (1=Pas du tout à 5=Beaucoup)")
        
        col1, col2 = st.columns(2)
        with col1:
            action = st.slider("Action/Aventure", 1, 5, 3)
            scifi = st.slider("Science-Fiction", 1, 5, 3)
            drame = st.slider("Drame", 1, 5, 3)
            comedie = st.slider("Comédie", 1, 5, 3)
        
        with col2:
            animation = st.slider("Animation", 1, 5, 3)
            horreur = st.slider("Horreur/Thriller", 1, 5, 3)
            romantique = st.slider("Romantique", 1, 5, 3)
            historique = st.slider("Historique", 1, 5, 3)
        
        st.subheader("🎬 Questions guidées")
        realisateurs_preferes = st.text_input("Réalisateurs préférés (séparés par des virgules)", 
                                               placeholder="Ex: Christopher Nolan, Quentin Tarantino")
        
        periode = st.selectbox("Période préférée", 
                               ["Aucune préférence", "Films classiques (avant 1980)", 
                                "Années 80-90", "Années 2000-2010", "Films récents (2010+)"])
        
        mood = st.multiselect("Ambiances recherchées",
                              ["Inspirant", "Sombre", "Drôle", "Émouvant", 
                               "Intense", "Relaxant", "Mystérieux", "Épique"])
        
        description_libre = st.text_area("Décrivez le type de films que vous aimez",
                                          placeholder="Ex: J'aime les films avec des rebondissements, des histoires complexes...")
        
        submitted = st.form_submit_button("💾 Sauvegarder mon profil")
        
        if submitted:
            st.session_state.user_profile = {
                "genres": {
                    "action": action,
                    "science-fiction": scifi,
                    "drame": drame,
                    "comedie": comedie,
                    "animation": animation,
                    "horreur": horreur,
                    "romantique": romantique,
                    "historique": historique
                },
                "realisateurs": realisateurs_preferes,
                "periode": periode,
                "mood": mood,
                "description": description_libre
            }
            st.session_state.show_profile_form = False
            st.success("✅ Profil sauvegardé avec succès !")
            st.rerun()

# Main content - only show if profile is configured
if not st.session_state.user_profile:
    st.info("👆 Créez votre profil dans la barre latérale pour commencer à recevoir des recommandations personnalisées.")
    st.stop()

# Show profile-based suggestions
st.title("🎬 Recommandations Personnalisées")

with st.spinner("Chargement de vos recommandations..."):
    try:
        response = requests.post(
            f"{API_URL}/suggestions",
            json={"user_profile": st.session_state.user_profile, "k": 4},
            timeout=10
        )
        if response.ok:
            suggestions = response.json().get("suggestions", [])
            
            if suggestions:
                st.subheader("📌 Films suggérés pour vous")
                
                cols = st.columns(4)
                
                for idx, movie in enumerate(suggestions):
                    with cols[idx]:
                        # Récupérer l'ID et construire le chemin
                        movie_id = movie.get("id")
                        
                        if movie_id:
                            base_dir = os.path.dirname(os.path.abspath(__file__))
                            local_image = os.path.join(base_dir, "data", "images", f"{movie_id}.jpg")
                            
                            # Charger et afficher l'image avec PIL
                            if os.path.exists(local_image):
                                try:
                                    img = Image.open(local_image)
                                    st.image(img, use_column_width=True)
                                except Exception as e:
                                    st.error(f"Erreur: {e}")
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                padding: 100px 20px; 
                                                border-radius: 10px; 
                                                text-align: center; 
                                                color: white;
                                                font-size: 36px;
                                                margin-bottom: 10px;">
                                        🎬
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                # Fallback si l'image n'existe pas
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                            padding: 100px 20px; 
                                            border-radius: 10px; 
                                            text-align: center; 
                                            color: white;
                                            font-size: 36px;
                                            margin-bottom: 10px;">
                                    🎬
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 100px 20px; 
                                        border-radius: 10px; 
                                        text-align: center; 
                                        color: white;
                                        font-size: 36px;
                                        margin-bottom: 10px;">
                                🎬
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown(f"**{movie['title']}**")
                        st.markdown(f"📅 {movie['year']}")
                        st.markdown(f"⭐ {movie['rating']}/10")
                        st.markdown(f"🎬 {movie['director']}")
                        with st.expander("📖 Synopsis"):
                            st.write(movie.get('description', 'Aucune description disponible'))
            else:
                st.info("Aucune suggestion disponible pour le moment.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des suggestions: {str(e)}")

st.markdown("---")


# Main content
tab1, tab2 = st.tabs(["💬 Chat", "🔍 Recherche"])

with tab1:
    st.header("Conversation avec l'Agent")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message" style="color: #000000;">
                    <b style="color: #000000;">👤 Vous:</b><br><span style="color: #000000;">{content}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message" style="color: #000000;">
                    <b style="color: #000000;">🤖 Assistant:</b><br><span style="color: #000000;">{content}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display source documents if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources utilisées"):
                        for i, source in enumerate(message["sources"], 1):
                            metadata = source.get("metadata", {})
                            st.markdown(f"""
                            <div class="source-doc" style="color: #000000;">
                                <b style="color: #000000;">Source {i}:</b> <span style="color: #000000;">{metadata.get('title', 'N/A')} 
                                ({metadata.get('year', 'N/A')}) - Note: {metadata.get('rating', 'N/A')}/10</span>
                            </div>
                            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input(
        "Votre message:",
        placeholder="Ex: Recommande-moi des films de science-fiction...",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        send_button = st.button("📤 Envoyer", use_container_width=True)
    
    if send_button and user_input:
        if not st.session_state.api_healthy:
            st.error("L'API n'est pas disponible. Vérifiez qu'elle est lancée.")
        else:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get response
            with st.spinner("Réflexion en cours..."):
                response = send_message(user_input)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"],
                "sources": response["source_documents"]
            })
            
            st.rerun()

with tab2:
    st.header("Recherche Sémantique de Films")
    st.markdown("Effectuez une recherche sémantique dans la base de données de films.")
    
    search_query = st.text_input(
        "Votre recherche:",
        placeholder="Ex: Films d'action avec des effets spéciaux époustouflants...",
        key="search_input"
    )
    
    num_results = st.slider("Nombre de résultats:", 1, 10, 5)
    
    if st.button("🔍 Rechercher", use_container_width=True):
        if not st.session_state.api_healthy:
            st.error("L'API n'est pas disponible. Vérifiez qu'elle est lancée.")
        elif search_query:
            with st.spinner("Recherche en cours..."):
                results = search_movies(search_query, num_results)
            
            if results["results"]:
                st.success(f"✅ {len(results['results'])} résultats trouvés")
                
                for i, result in enumerate(results["results"], 1):
                    with st.expander(f"🎬 Résultat {i}"):
                        metadata = result.get("metadata", {})
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"**Titre:** {metadata.get('title', 'N/A')}")
                            st.markdown(f"**Année:** {metadata.get('year', 'N/A')}")
                            st.markdown(f"**Réalisateur:** {metadata.get('director', 'N/A')}")
                        with col2:
                            rating = metadata.get('rating', 0)
                            st.metric("Note", f"{rating}/10")
                        
                        st.markdown("**Description:**")
                        st.text(result.get("content", ""))
            else:
                st.warning("Aucun résultat trouvé.")
        else:
            st.warning("Veuillez entrer une recherche.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Agent Intelligent Sémantique et Génératif - Projet IA 2026
</div>
""", unsafe_allow_html=True)

# Auto-check API health on startup
if not st.session_state.api_healthy:
    st.session_state.api_healthy = check_api_health()
