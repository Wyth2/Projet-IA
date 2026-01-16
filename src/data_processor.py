"""Data processing module for movie recommendations."""
import pandas as pd
from typing import List, Dict, Any
import json
import os


class MovieDataProcessor:
    """Process and manage movie data."""
    
    def __init__(self):
        """Initialize the movie data processor."""
        self.movies_data = []
        
    def load_sample_movies(self) -> List[Dict[str, Any]]:
        """
        Load movie data from TMDB JSON file if available, otherwise use sample data.
        
        Returns:
            List of movie dictionaries
        """
        # Try to load from TMDB JSON first
        tmdb_file = "data/tmdb_movies.json"
        if os.path.exists(tmdb_file):
            try:
                with open(tmdb_file, 'r', encoding='utf-8') as f:
                    self.movies_data = json.load(f)
                print(f"✓ Loaded {len(self.movies_data)} movies from TMDB dataset")
                return self.movies_data
            except Exception as e:
                print(f"Warning: Could not load TMDB data: {e}")
        
        # Fallback to sample data
        print("✓ Using sample movies (run fetch_tmdb_movies.py to get more movies)")
        self.movies_data = [
            {
                "id": 1,
                "title": "The Shawshank Redemption",
                "year": 1994,
                "genre": ["Drama"],
                "director": "Frank Darabont",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "rating": 9.3,
                "actors": ["Tim Robbins", "Morgan Freeman"],
                "image_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
            },
            {
                "id": 2,
                "title": "The Godfather",
                "year": 1972,
                "genre": ["Crime", "Drama"],
                "director": "Francis Ford Coppola",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "rating": 9.2,
                "actors": ["Marlon Brando", "Al Pacino"],
                "image_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
            },
            {
                "id": 3,
                "title": "The Dark Knight",
                "year": 2008,
                "genre": ["Action", "Crime", "Drama"],
                "director": "Christopher Nolan",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
                "rating": 9.0,
                "actors": ["Christian Bale", "Heath Ledger"],
                "image_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
            },
            {
                "id": 4,
                "title": "Pulp Fiction",
                "year": 1994,
                "genre": ["Crime", "Drama"],
                "director": "Quentin Tarantino",
                "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
                "rating": 8.9,
                "actors": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                "image_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"
            },
            {
                "id": 5,
                "title": "Forrest Gump",
                "year": 1994,
                "genre": ["Drama", "Romance"],
                "director": "Robert Zemeckis",
                "description": "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man with an IQ of 75.",
                "rating": 8.8,
                "actors": ["Tom Hanks", "Robin Wright"],
                "image_url": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"
            },
            {
                "id": 6,
                "title": "Inception",
                "year": 2010,
                "genre": ["Action", "Sci-Fi", "Thriller"],
                "director": "Christopher Nolan",
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                "rating": 8.8,
                "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
                "image_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"
            },
            {
                "id": 7,
                "title": "The Matrix",
                "year": 1999,
                "genre": ["Action", "Sci-Fi"],
                "director": "Lana Wachowski, Lilly Wachowski",
                "description": "A computer hacker learns about the true nature of reality and his role in the war against its controllers.",
                "rating": 8.7,
                "actors": ["Keanu Reeves", "Laurence Fishburne"],
                "image_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
            },
            {
                "id": 8,
                "title": "Interstellar",
                "year": 2014,
                "genre": ["Adventure", "Drama", "Sci-Fi"],
                "director": "Christopher Nolan",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "rating": 8.6,
                "actors": ["Matthew McConaughey", "Anne Hathaway"],
                "image_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
            },
            {
                "id": 9,
                "title": "Parasite",
                "year": 2019,
                "genre": ["Comedy", "Drama", "Thriller"],
                "director": "Bong Joon Ho",
                "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                "rating": 8.6,
                "actors": ["Song Kang-ho", "Lee Sun-kyun"],
                "image_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
            },
            {
                "id": 10,
                "title": "The Prestige",
                "year": 2006,
                "genre": ["Drama", "Mystery", "Thriller"],
                "director": "Christopher Nolan",
                "description": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion.",
                "rating": 8.5,
                "actors": ["Christian Bale", "Hugh Jackman"],
                "image_url": "https://image.tmdb.org/t/p/w500/tRNlZbgNCNOpLpbPEz5L8G8A0JN.jpg"
            },
            {
                "id": 11,
                "title": "Gladiator",
                "year": 2000,
                "genre": ["Action", "Adventure", "Drama"],
                "director": "Ridley Scott",
                "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family.",
                "rating": 8.5,
                "actors": ["Russell Crowe", "Joaquin Phoenix"],
                "image_url": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"
            },
            {
                "id": 12,
                "title": "The Departed",
                "year": 2006,
                "genre": ["Crime", "Drama", "Thriller"],
                "director": "Martin Scorsese",
                "description": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang.",
                "rating": 8.5,
                "actors": ["Leonardo DiCaprio", "Matt Damon", "Jack Nicholson"],
                "image_url": "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg"
            }
        ]
        
        return self.movies_data
    
    def get_movie_text(self, movie: Dict[str, Any]) -> str:
        """
        Convert movie data to text format for embedding.
        
        Args:
            movie: Movie dictionary
            
        Returns:
            Formatted text representation of the movie
        """
        text = f"Title: {movie['title']}\n"
        text += f"Year: {movie['year']}\n"
        text += f"Genre: {', '.join(movie['genre'])}\n"
        text += f"Director: {movie['director']}\n"
        text += f"Description: {movie['description']}\n"
        text += f"Rating: {movie['rating']}/10\n"
        text += f"Actors: {', '.join(movie['actors'])}\n"
        
        return text
    
    def format_movies_for_rag(self) -> List[Dict[str, str]]:
        """
        Format movies for RAG system.
        
        Returns:
            List of formatted movie documents
        """
        documents = []
        for movie in self.movies_data:
            # Prepare metadata without None values
            # Convert id to int to ensure it's stored correctly
            metadata = {
                "id": int(movie["id"]),
                "title": movie["title"],
                "year": str(movie["year"]),
                "genre": json.dumps(movie["genre"]),
                "director": movie["director"],
                "rating": float(movie["rating"])
            }
            
            # Add optional fields only if they exist and are not None
            if movie.get("image_url"):
                metadata["image_url"] = movie["image_url"]
            if movie.get("local_image_path"):
                metadata["local_image_path"] = movie["local_image_path"]
            
            doc = {
                "content": self.get_movie_text(movie),
                "metadata": metadata
            }
            documents.append(doc)
        
        return documents
