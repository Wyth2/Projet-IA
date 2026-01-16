"""Fetch movies from TMDB API and update the database."""
import requests
import json
import os
from pathlib import Path
from src.data_processor import MovieDataProcessor
from src.rag_system import RAGSystem

# TMDB API Configuration (free API key)
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"  # Free public key for testing
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
LOCAL_IMAGE_DIR = Path("data/images")

def download_image(image_url, movie_id):
    """Download movie poster locally."""
    if not image_url:
        return None
    
    try:
        LOCAL_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        local_path = LOCAL_IMAGE_DIR / f"{movie_id}.jpg"
        
        # Download image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Save locally
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✓ Image downloaded: {local_path.name}")
        return str(local_path)
    except Exception as e:
        print(f"  ✗ Image download error {movie_id}: {e}")
        return None

def fetch_popular_movies(num_pages=5):
    """Fetch popular movies from TMDB."""
    movies = []
    
    for page in range(1, num_pages + 1):
        url = f"{TMDB_BASE_URL}/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "page": page
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for movie in data.get("results", []):
                # Get movie details for more info
                movie_id = movie["id"]
                details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
                details_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "fr-FR"
                }
                
                details_response = requests.get(details_url, params=details_params, timeout=10)
                if details_response.ok:
                    details = details_response.json()
                    
                    # Get credits for director and actors
                    credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
                    credits_response = requests.get(credits_url, params={"api_key": TMDB_API_KEY}, timeout=10)
                    credits = credits_response.json() if credits_response.ok else {}
                    
                    # Extract director
                    director = "Unknown"
                    crew = credits.get("crew", [])
                    for member in crew:
                        if member.get("job") == "Director":
                            director = member.get("name", "Unknown")
                            break
                    
                    # Extract top actors
                    cast = credits.get("cast", [])
                    actors = [actor.get("name") for actor in cast[:3]]
                    
                    # Extract genres
                    genres = [g["name"] for g in details.get("genres", [])]
                    
                    # Download image locally
                    image_url = f"{TMDB_IMAGE_BASE}{movie['poster_path']}" if movie.get("poster_path") else ""
                    local_image_path = download_image(image_url, movie_id)
                    
                    movie_data = {
                        "id": movie_id,
                        "title": details.get("title", movie.get("title", "Unknown")),
                        "year": details.get("release_date", "")[:4] if details.get("release_date") else "N/A",
                        "genre": genres,
                        "director": director,
                        "description": details.get("overview", movie.get("overview", "No description available")),
                        "rating": round(details.get("vote_average", 0), 1),
                        "actors": actors,
                        "image_url": image_url,
                        "local_image_path": local_image_path
                    }
                    
                    movies.append(movie_data)
                    print(f"✓ Loaded: {movie_data['title']} ({movie_data['year']})")
            
            print(f"Page {page}/{num_pages} completed")
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
    
    return movies


def save_to_json(movies, filename="data/tmdb_movies.json"):
    """Save movies to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Saved {len(movies)} movies to {filename}")


def update_database(movies):
    """Update the vector database with TMDB movies."""
    print("\nInitializing RAG system...")
    rag_system = RAGSystem()
    
    # Create processor and set movies data
    processor = MovieDataProcessor()
    processor.movies_data = movies
    
    # Initialize vectorstore with TMDB data
    print("Indexing movies in vector database...")
    rag_system.initialize_vectorstore()
    
    print("✓ Database updated successfully!")


if __name__ == "__main__":
    print("=" * 60)
    print("Fetching movies from TMDB API")
    print("=" * 60)
    
    # Fetch 5 pages (about 100 movies)
    movies = fetch_popular_movies(num_pages=5)
    
    print(f"\n✓ Total movies fetched: {len(movies)}")
    
    # Save to JSON
    save_to_json(movies)
    
    # Update vector database
    update_choice = input("\nUpdate vector database with these movies? (y/n): ")
    if update_choice.lower() == 'y':
        update_database(movies)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
