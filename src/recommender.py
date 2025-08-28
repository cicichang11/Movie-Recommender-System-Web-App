import numpy as np
import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class HybridRecommender:
    def __init__(self, movies_data, credits_data):
        """
        Initialize the hybrid recommender system
        
        Args:
            movies_data: Path to movies CSV file
            credits_data: Path to credits CSV file
        """
        self.movies_data = movies_data
        self.credits_data = credits_data
        self.movies_df = None
        self.credits_df = None
        self.processed_df = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.svd_model = None
        self.user_movie_matrix = None
        self.scaler = StandardScaler()
        
    def load_and_preprocess_data(self):
        """Load and preprocess the movie and credits data"""
        print("Loading data...")
        self.movies_df = pd.read_csv(self.movies_data)
        self.credits_df = pd.read_csv(self.credits_data)
        
        print("Preprocessing data...")
        # Merge datasets
        self.processed_df = self.movies_df.merge(self.credits_df, on='title')
        
        # Select relevant columns
        self.processed_df = self.processed_df[['movie_id', 'title', 'overview', 'genres', 
                                              'keywords', 'cast', 'crew', 'vote_average', 
                                              'vote_count', 'popularity', 'release_date']]
        
        # Handle missing values
        self.processed_df.dropna(subset=['overview', 'genres', 'keywords'], inplace=True)
        
        # Convert string representations to lists
        self.processed_df['genres'] = self.processed_df['genres'].apply(self._parse_json_column)
        self.processed_df['keywords'] = self.processed_df['keywords'].apply(self._parse_json_column)
        self.processed_df['cast'] = self.processed_df['cast'].apply(self._parse_cast_column)
        self.processed_df['crew'] = self.processed_df['crew'].apply(self._parse_crew_column)
        
        # Create enhanced tags
        self.processed_df['tags'] = self.processed_df.apply(self._create_tags, axis=1)
        
        # Create user-movie interaction matrix (simulated)
        self._create_user_movie_matrix()
        
        print(f"Processed {len(self.processed_df)} movies")
        
    def _parse_json_column(self, text):
        """Parse JSON-like string columns"""
        try:
            import ast
            data = ast.literal_eval(text)
            if isinstance(data, list):
                return [item.get('name', '') for item in data if item.get('name')]
            return []
        except:
            return []
    
    def _parse_cast_column(self, text):
        """Parse cast column and get top 3 actors"""
        try:
            import ast
            data = ast.literal_eval(text)
            if isinstance(data, list):
                return [item.get('name', '') for item in data[:3] if item.get('name')]
            return []
        except:
            return []
    
    def _parse_crew_column(self, text):
        """Parse crew column and get directors"""
        try:
            import ast
            data = ast.literal_eval(text)
            if isinstance(data, list):
                directors = [item.get('name', '') for item in data if item.get('job') == 'Director']
                return directors[:2]  # Get up to 2 directors
            return []
        except:
            return []
    
    def _create_tags(self, row):
        """Create comprehensive tags for each movie"""
        tags = []
        
        # Add overview words
        if pd.notna(row['overview']):
            tags.extend(str(row['overview']).lower().split()[:20])  # Limit to first 20 words
        
        # Add genres
        tags.extend([genre.lower().replace(' ', '') for genre in row['genres']])
        
        # Add keywords
        tags.extend([keyword.lower().replace(' ', '') for keyword in row['keywords']])
        
        # Add cast
        tags.extend([actor.lower().replace(' ', '') for actor in row['cast']])
        
        # Add crew (directors)
        tags.extend([director.lower().replace(' ', '') for director in row['crew']])
        
        return ' '.join(tags)
    
    def _create_user_movie_matrix(self):
        """Create a simulated user-movie interaction matrix"""
        print("Creating user-movie interaction matrix...")
        
        # Create synthetic user ratings based on movie popularity and vote average
        np.random.seed(42)  # For reproducibility
        
        n_users = 1000  # Simulate 1000 users
        n_movies = len(self.processed_df)
        
        # Create base ratings based on movie popularity and vote average
        base_ratings = []
        for _, movie in self.processed_df.iterrows():
            # Normalize popularity and vote average to 0-1 scale
            popularity_norm = min(movie['popularity'] / 100, 1.0)
            vote_avg_norm = movie['vote_average'] / 10.0
            
            # Combine them with weights
            base_rating = 0.6 * popularity_norm + 0.4 * vote_avg_norm
            
            # Add some randomness
            base_rating += np.random.normal(0, 0.1)
            base_rating = np.clip(base_rating, 0, 1)
            
            base_ratings.append(base_rating)
        
        # Create user-movie matrix
        self.user_movie_matrix = np.zeros((n_users, n_movies))
        
        for user in range(n_users):
            # Each user rates a random subset of movies
            n_ratings = np.random.randint(10, 50)  # User rates 10-50 movies
            rated_movies = np.random.choice(n_movies, n_ratings, replace=False)
            
            for movie_idx in rated_movies:
                # Add user-specific variation to base rating
                user_rating = base_ratings[movie_idx] + np.random.normal(0, 0.2)
                user_rating = np.clip(user_rating, 0, 1)
                
                # Convert to 1-5 scale
                self.user_movie_matrix[user, movie_idx] = int(user_rating * 5) + 1
        
        print(f"Created user-movie matrix: {self.user_movie_matrix.shape}")
    
    def build_content_based_model(self):
        """Build the content-based recommendation model"""
        print("Building content-based model...")
        
        # Use TF-IDF instead of CountVectorizer for better text representation
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english', 
                               ngram_range=(1, 2), min_df=2)
        
        self.tfidf_matrix = tfidf.fit_transform(self.processed_df['tags'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        print("Content-based model built successfully")
    
    def build_collaborative_model(self):
        """Build the collaborative filtering model using SVD"""
        print("Building collaborative filtering model...")
        
        # Apply SVD to the user-movie matrix
        self.svd_model = TruncatedSVD(n_components=50, random_state=42)
        
        # Fit the model
        self.svd_model.fit(self.user_movie_matrix)
        
        print("Collaborative filtering model built successfully")
    
    def get_content_based_recommendations(self, movie_title, n_recommendations=5):
        """Get content-based recommendations"""
        try:
            movie_idx = self.processed_df[self.processed_df['title'] == movie_title].index[0]
            movie_similarities = self.similarity_matrix[movie_idx]
            
            # Get top similar movies (excluding the movie itself)
            similar_indices = np.argsort(movie_similarities)[::-1][1:n_recommendations+1]
            
            recommendations = []
            for idx in similar_indices:
                movie_info = self.processed_df.iloc[idx]
                recommendations.append({
                    'title': movie_info['title'],
                    'similarity_score': movie_similarities[idx],
                    'genres': movie_info['genres'],
                    'vote_average': movie_info['vote_average'],
                    'overview': movie_info['overview'][:100] + '...' if len(str(movie_info['overview'])) > 100 else movie_info['overview']
                })
            
            return recommendations
        except:
            return []
    
    def get_collaborative_recommendations(self, user_id, n_recommendations=5):
        """Get collaborative filtering recommendations for a user"""
        try:
            # Get user's movie ratings
            user_ratings = self.user_movie_matrix[user_id]
            
            # Find movies the user hasn't rated (rating == 0)
            unrated_movies = np.where(user_ratings == 0)[0]
            
            if len(unrated_movies) == 0:
                return []
            
            # Predict ratings for unrated movies
            predicted_ratings = self.svd_model.transform(user_ratings.reshape(1, -1))
            reconstructed_ratings = self.svd_model.inverse_transform(predicted_ratings).flatten()
            
            # Get predicted ratings for unrated movies
            unrated_predictions = reconstructed_ratings[unrated_movies]
            
            # Get top recommendations
            top_indices = np.argsort(unrated_predictions)[::-1][:n_recommendations]
            recommended_movies = unrated_movies[top_indices]
            
            recommendations = []
            for idx in recommended_movies:
                movie_info = self.processed_df.iloc[idx]
                recommendations.append({
                    'title': movie_info['title'],
                    'predicted_rating': reconstructed_ratings[idx],
                    'genres': movie_info['genres'],
                    'vote_average': movie_info['vote_average'],
                    'overview': movie_info['overview'][:100] + '...' if len(str(movie_info['overview'])) > 100 else movie_info['overview']
                })
            
            return recommendations
        except:
            return []
    
    def get_hybrid_recommendations(self, movie_title=None, user_id=None, n_recommendations=5):
        """Get hybrid recommendations combining both approaches"""
        content_recs = []
        collaborative_recs = []
        
        # Get content-based recommendations if movie title is provided
        if movie_title:
            content_recs = self.get_content_based_recommendations(movie_title, n_recommendations)
        
        # Get collaborative recommendations if user_id is provided
        if user_id is not None:
            collaborative_recs = self.get_collaborative_recommendations(user_id, n_recommendations)
        
        # Combine recommendations
        if content_recs and collaborative_recs:
            # Hybrid approach: combine and re-rank
            all_recs = content_recs + collaborative_recs
            
            # Remove duplicates based on title
            seen_titles = set()
            unique_recs = []
            for rec in all_recs:
                if rec['title'] not in seen_titles:
                    seen_titles.add(rec['title'])
                    unique_recs.append(rec)
            
            # Sort by a combined score
            for rec in unique_recs:
                if 'similarity_score' in rec:
                    rec['combined_score'] = rec['similarity_score']
                elif 'predicted_rating' in rec:
                    rec['combined_score'] = rec['predicted_rating'] / 5.0  # Normalize to 0-1
            
            unique_recs.sort(key=lambda x: x.get('combined_score', 0), reverse=True)
            return unique_recs[:n_recommendations]
        
        elif content_recs:
            return content_recs
        elif collaborative_recs:
            return collaborative_recs
        else:
            return []
    
    def save_models(self, output_dir='artifacts'):
        """Save all models and data for later use"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("Saving models...")
        
        # Save processed data
        with open(f'{output_dir}/processed_movies.pkl', 'wb') as f:
            pickle.dump(self.processed_df, f)
        
        # Save similarity matrix
        with open(f'{output_dir}/similarity_matrix.pkl', 'wb') as f:
            pickle.dump(self.similarity_matrix, f)
        
        # Save TF-IDF matrix
        with open(f'{output_dir}/tfidf_matrix.pkl', 'wb') as f:
            pickle.dump(self.tfidf_matrix, f)
        
        # Save SVD model
        with open(f'{output_dir}/svd_model.pkl', 'wb') as f:
            pickle.dump(self.svd_model, f)
        
        # Save user-movie matrix
        with open(f'{output_dir}/user_movie_matrix.pkl', 'wb') as f:
            pickle.dump(self.user_movie_matrix, f)
        
        print(f"Models saved to {output_dir}")
    
    def load_models(self, input_dir='artifacts'):
        """Load pre-trained models and data"""
        print("Loading models...")
        
        try:
            with open(f'{input_dir}/processed_movies.pkl', 'rb') as f:
                self.processed_df = pickle.load(f)
            
            with open(f'{input_dir}/similarity_matrix.pkl', 'rb') as f:
                self.similarity_matrix = pickle.load(f)
            
            with open(f'{input_dir}/tfidf_matrix.pkl', 'rb') as f:
                self.tfidf_matrix = pickle.load(f)
            
            with open(f'{input_dir}/svd_model.pkl', 'rb') as f:
                self.svd_model = pickle.load(f)
            
            with open(f'{input_dir}/user_movie_matrix.pkl', 'rb') as f:
                self.user_movie_matrix = pickle.load(f)
            
            print("Models loaded successfully")
            return True
        except FileNotFoundError:
            print("Model files not found. Please train the model first.")
            return False
