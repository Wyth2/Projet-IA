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
    page_icon="📽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 3rem 2rem;
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        backdrop-filter: blur(10px);
    }
    
    /* Force text colors for visibility */
    .block-container p, .block-container span, .block-container div {
        color: #2c3e50 !important;
    }
    
    /* Additional text visibility rules */
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #2c3e50 !important;
    }
    
    .stText, .stCaption {
        color: #2c3e50 !important;
    }
    
    /* Form elements */
    .stTextInput label, .stSelectbox label, .stSlider label, .stMultiSelect label {
        color: #2c3e50 !important;
        font-weight: 500;
    }
    
    h1 {
        color: #2c3e50;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    h2, h3 {
        color: #34495e;
        font-weight: 600;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px 16px;
        color: #2c3e50 !important;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #7f8c8d !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #5a6c7d 0%, #34495e 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(52, 73, 94, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(52, 73, 94, 0.4);
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: #34495e;
        color: #ffffff !important;
        border-left: 5px solid #2c3e50;
    }
    
    .user-message b {
        color: #ffffff !important;
    }
    
    .user-message span {
        color: #ffffff !important;
    }
    
    .assistant-message {
        background: #ecf0f1;
        color: #2c3e50 !important;
        border-left: 5px solid #7f8c8d;
    }
    
    .assistant-message b {
        color: #2c3e50 !important;
    }
    
    .assistant-message span {
        color: #2c3e50 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5a6c7d 0%, #34495e 100%);
        color: white;
    }
    
    .stExpander {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        border-color: #5a6c7d;
        box-shadow: 0 4px 12px rgba(90, 108, 125, 0.15);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
        color: white;
    }
    
    .stSidebar > div {
        background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: white !important;
    }
    
    .stSidebar .stMarkdown {
        color: white !important;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #5a6c7d 0%, #34495e 100%);
    }
    
    .stSuccess {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 8px;
        padding: 12px;
    }
    
    .stError {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 8px;
        padding: 12px;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 8px;
        padding: 12px;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 8px;
        padding: 12px;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #34495e;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #bdc3c7, transparent);
    }
    
    /* Ensure all Streamlit elements have visible text */
    .stMarkdown, .stText, label, .stSelectbox label, .stSlider label {
        color: #2c3e50 !important;
    }
    
    .movie-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(52, 73, 94, 0.3);
        border-color: #5a6c7d;
    }
    
    .movie-card img {
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .movie-card:hover img {
        transform: scale(1.05);
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
st.title("CinéMind - Votre conseiller cinéma intelligent")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # Check API status
    if st.button("Vérifier l'API"):
        st.session_state.api_healthy = check_api_health()
    
    if st.session_state.api_healthy:
        st.success("API connectée")
    else:
        st.error("API non disponible")
        st.info("Lancez l'API avec: `python api.py`")
    
    st.markdown("---")
    
    # User Profile Section
    st.header("Profil Utilisateur")
    if st.session_state.user_profile:
        st.success("Profil configuré")
        if st.button("Modifier le profil"):
            st.session_state.show_profile_form = True
            st.rerun()
    else:
        st.warning("Aucun profil configuré")
        if st.button("Créer mon profil"):
            st.session_state.show_profile_form = True
            st.rerun()
    
    st.markdown("---")
    
    # Reset conversation
    if st.button("Réinitialiser la conversation"):
        if reset_conversation():
            st.success("Conversation réinitialisée!")
            st.rerun()
        else:
            st.error("Erreur lors de la réinitialisation")
    
    st.markdown("---")
    
    st.header("À propos")
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
    st.title("Création de votre Profil Cinématographique")
    st.markdown("Répondez à ces quelques questions pour personnaliser vos recommandations.")
    
    with st.form("profile_form"):
        st.subheader("Préférences par Genre (1=Pas du tout à 5=Beaucoup)")
        
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
        
        st.subheader("Questions guidées")
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
        
        submitted = st.form_submit_button("Sauvegarder mon profil")
        
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
            st.success("Profil sauvegardé avec succès !")
            st.rerun()

# Main content - only show if profile is configured
if not st.session_state.user_profile:
    st.info("Créez votre profil dans la barre latérale pour commencer à recevoir des recommandations personnalisées.")
    st.stop()

# Show profile-based suggestions
st.title("Recommandations Personnalisées")

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
                st.subheader("Films suggérés pour vous")
                
                cols = st.columns(4)
                
                for idx, movie in enumerate(suggestions):
                    with cols[idx]:
                        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                        # Récupérer l'ID et construire le chemin
                        movie_id = movie.get("id")
                        
                        if movie_id:
                            base_dir = os.path.dirname(os.path.abspath(__file__))
                            local_image = os.path.join(base_dir, "data", "images", f"{movie_id}.jpg")
                            
                            # Charger et afficher l'image avec PIL
                            if os.path.exists(local_image):
                                try:
                                    img = Image.open(local_image)
                                    st.image(img, use_container_width=True)
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
                        
                        st.markdown(f"<h3 style='color: #34495e; margin: 1rem 0 0.5rem 0;'>{movie['title']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #7f8c8d; margin: 0.25rem 0;'>Année : {movie['year']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #f39c12; margin: 0.25rem 0; font-weight: 600;'>Note : {movie['rating']}/10</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #95a5a6; margin: 0.25rem 0;'>Réalisateur : {movie['director']}</p>", unsafe_allow_html=True)
                        with st.expander("Synopsis"):
                            st.write(movie.get('description', 'Aucune description disponible'))
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Aucune suggestion disponible pour le moment.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des suggestions: {str(e)}")

st.markdown("---")


# Main content
tab1, tab2 = st.tabs(["Chat", "Recherche"])

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
                <div class="chat-message user-message">
                    <b style="color: #ffffff !important; font-size: 1.1rem;">💬 Vous</b><br>
                    <span style="color: #ffffff !important; font-size: 1rem; line-height: 1.6;">{content}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Afficher les images des films recommandés en premier
                if "movie_images" in message and message["movie_images"]:
                    st.markdown("**Films recommandés:**")
                    cols = st.columns(min(len(message["movie_images"]), 4))
                    for idx, movie_img in enumerate(message["movie_images"]):
                        with cols[idx % len(cols)]:
                            try:
                                img = Image.open(movie_img["path"])
                                st.image(img, caption=movie_img["title"], use_container_width=True)
                            except:
                                st.info(f"{movie_img['title']}")
                    st.markdown("")  # Espace
                
                # Afficher le texte de la réponse en dessous
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <b style="color: #2c3e50 !important; font-size: 1.1rem;">🤖 Assistant</b><br>
                    <span style="color: #2c3e50 !important; font-size: 1rem; line-height: 1.6;">{content}</span>
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
        send_button = st.button("Envoyer", use_container_width=True)
    
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
            
            # Add assistant message with movie images from sources
            movie_images = []
            for source in response["source_documents"]:
                movie_id = source.get("metadata", {}).get("id")
                if movie_id:
                    local_image = f"data/images/{movie_id}.jpg"
                    if os.path.exists(local_image):
                        movie_images.append({
                            "id": movie_id,
                            "title": source.get("metadata", {}).get("title", "Film"),
                            "path": local_image
                        })
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"],
                "sources": response["source_documents"],
                "movie_images": movie_images
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
    
    if st.button("Rechercher", use_container_width=True):
        if not st.session_state.api_healthy:
            st.error("L'API n'est pas disponible. Vérifiez qu'elle est lancée.")
        elif search_query:
            with st.spinner("Recherche en cours..."):
                results = search_movies(search_query, num_results)
            
            if results["results"]:
                st.success(f"{len(results['results'])} résultats trouvés")
                
                for i, result in enumerate(results["results"], 1):
                    with st.expander(f"Résultat {i}"):
                        metadata = result.get("metadata", {})
                        
                        col1, col2 = st.columns([3, 2])
                        with col1:
                            st.markdown(f"**Titre:** {metadata.get('title', 'N/A')}")
                            st.markdown(f"**Année:** {metadata.get('year', 'N/A')}")
                            st.markdown(f"**Réalisateur:** {metadata.get('director', 'N/A')}")
                            rating = metadata.get('rating', 0)
                            st.metric("Note", f"{rating}/10")
                        
                        with col2:
                            # Afficher l'image du film
                            movie_id = metadata.get('id')
                            if movie_id:
                                local_image = f"data/images/{movie_id}.jpg"
                                if os.path.exists(local_image):
                                    try:
                                        img = Image.open(local_image)
                                        st.image(img, use_container_width=True)
                                    except:
                                        st.info("Image non disponible")
                        
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
