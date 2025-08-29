import streamlit as st
import pickle
import requests
import pandas as pd
import numpy as np
from PIL import Image
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from recommender import HybridRecommender

# Page configuration
st.set_page_config(
    page_title="🎬 Hybrid Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/movie-recommender',
        'Report a bug': "https://github.com/yourusername/movie-recommender/issues",
        'About': "# 🎬 Hybrid Movie Recommender\n\nA sophisticated movie recommendation system combining content-based and collaborative filtering approaches."
    }
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Modern Color Palette - 2024 Trends */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #10b981;
        --accent: #f59e0b;
        --success: #06b6d4;
        --warning: #ef4444;
        --dark: #1f2937;
        --light: #f8fafc;
        --gray: #6b7280;
        --border: #e5e7eb;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .sub-header {
        font-size: 1.75rem;
        color: var(--dark);
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* Modern Movie Cards */
    .movie-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--border);
        padding: 1.5rem;
        border-radius: 16px;
        color: var(--dark);
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    .movie-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: var(--primary);
    }
    
    /* Enhanced Recommendation Sections */
    .recommendation-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--border);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
        min-height: 0; /* Prevent empty sections from taking space */
    }
    
    .recommendation-section:empty {
        display: none !important; /* Hide completely empty sections */
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }
    
    /* Hide sections that only contain whitespace or minimal content */
    .recommendation-section:has(:only-child:empty) {
        display: none !important;
    }
    
    .recommendation-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 0 3px 3px 0;
        display: none; /* Hide the pseudo-element by default */
    }
    
    .recommendation-section:not(:empty)::before {
        display: block; /* Only show when there's content */
    }
    
    /* Modern Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--border);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::after {
        transform: scaleX(1);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
    }
    
    /* Enhanced Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Enhanced Slider */
    .stSlider > div > div > div > div {
        background: var(--primary);
    }
    
    .stSlider > div > div > div > div > div {
        background: var(--primary);
        border: 2px solid white;
        box-shadow: 0 0 0 2px var(--primary);
    }
    
    /* Slider number styling */
    .stSlider > div > div > div > div > div > div {
        color: var(--primary) !important;
        font-weight: 600;
    }
    
    /* Slider track and thumb */
    .stSlider > div > div > div > div > div > div > div {
        background: var(--primary) !important;
    }
    
    /* Slider value display */
    .stSlider > div > div > div > div > div > div > div > div {
        color: white !important;
        font-weight: 500;
        background: var(--primary);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        border: 1px solid var(--primary);
    }
    
    /* Override Streamlit's default red color for slider values */
    .stSlider [data-baseweb="slider"] [data-testid="stSlider"] > div > div > div > div > div > div > div > div {
        color: white !important;
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* Additional slider value overrides for different Streamlit versions */
    .stSlider [data-baseweb="slider"] > div > div > div > div > div > div > div > div {
        color: white !important;
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* Global slider value styling */
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div > div > div > div > div > div {
        color: white !important;
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
    }
    
    /* Slider label and range numbers should be black */
    .stSlider > div > div > div > div > div > div > div > div > div {
        color: var(--dark) !important; /* Black for range numbers (3, 15) */
    }
    
    /* Slider label text should be black */
    .stSlider > div > div > div > div > div > div > div > div > span {
        color: var(--dark) !important; /* Black for "Number of recommendations:" */
    }
    
    /* Only the current value display should be white on indigo */
    .stSlider [data-baseweb="slider"] > div > div > div > div > div > div > div > div {
        color: white !important; /* White for current value */
        background: var(--primary) !important; /* Indigo background */
        border: 1px solid var(--primary) !important;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid var(--border);
    }
    
    /* Text Enhancements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border: 3px solid var(--border);
        border-top: 3px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .sub-header {
            font-size: 1.5rem;
        }
        
        .movie-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_models():
    """Load pre-trained models"""
    try:
        recommender = HybridRecommender(
            movies_data='data/tmdb_5000_movies.csv',
            credits_data='data/tmdb_5000_credits.csv'
        )
        
        if recommender.load_models('artifacts'):
            return recommender
        else:
            st.error("❌ Model files not found. Please run the training script first.")
            st.info("Run: python train_model.py")
            return None
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    try:
        # Convert movie_id to string and handle any data type issues
        movie_id_str = str(int(movie_id)) if movie_id is not None else "0"
        url = f"https://api.themoviedb.org/3/movie/{movie_id_str}?api_key=a9877c59cb8681f7faf7075a75b22103&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path')
        
        if poster_path:
            full_path = f"http://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return None
    except:
        return None

def display_movie_card(movie_info, poster_url=None, score_info=None):
    """Display a movie card with information"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if poster_url:
                st.image(poster_url, width=150)
            else:
                st.image("https://via.placeholder.com/150x225/cccccc/666666?text=No+Poster", width=150)
        
        with col2:
            st.markdown(f"### {movie_info['title']}")
            
            # Display genres
            if 'genres' in movie_info and movie_info['genres']:
                genres_text = ", ".join(movie_info['genres'][:3])
                st.markdown(f"**Genres:** {genres_text}")
            
            # Display overview
            if 'overview' in movie_info and movie_info['overview']:
                overview = str(movie_info['overview'])
                if len(overview) > 200:
                    overview = overview[:200] + "..."
                st.markdown(f"**Overview:** {overview}")
            
            # Display score information
            if score_info:
                if 'similarity_score' in score_info:
                    st.markdown(f"**Similarity Score:** {score_info['similarity_score']:.3f}")
                elif 'predicted_rating' in score_info:
                    st.markdown(f"**Predicted Rating:** {score_info['predicted_rating']:.2f}/5.0")
            
            # Display vote average if available
            if 'vote_average' in movie_info and pd.notna(movie_info['vote_average']):
                st.markdown(f"**TMDB Rating:** ⭐ {movie_info['vote_average']:.1f}/10")

def main():
    """Main application function"""
    # Header
    st.markdown('<h1 class="main-header">🎬 Hybrid Movie Recommender</h1>', unsafe_allow_html=True)
    
    # Load models
    recommender = load_models()
    if recommender is None:
        return
    
    # Sidebar
    st.sidebar.markdown("## 🎯 Recommendation Mode")
    mode = st.sidebar.selectbox(
        "Choose your recommendation approach:",
        ["🎭 Content-Based", "👥 Collaborative Filtering", "🚀 Hybrid", "📊 System Info"]
    )
    
    # Main content area
    if mode == "🎭 Content-Based":
        st.markdown('<h2 class="sub-header">🎭 Content-Based Recommendations</h2>', unsafe_allow_html=True)
        st.markdown("Get movie recommendations based on content similarity (genres, cast, crew, keywords, overview).")
        
        # Movie selection
        movie_list = recommender.processed_df['title'].values.tolist()
        # Find default index safely
        default_index = 0
        try:
            if "Spider-Man" in movie_list:
                default_index = movie_list.index("Spider-Man")
        except:
            default_index = 0
            
        selected_movie = st.selectbox(
            'Select a movie you like:',
            movie_list,
            index=default_index
        )
        
        # Number of recommendations
        n_recommendations = st.slider("Number of recommendations:", 3, 10, 5)
        
        if st.button("🎬 Get Content-Based Recommendations", type="primary"):
            with st.spinner("Finding similar movies..."):
                recommendations = recommender.get_content_based_recommendations(selected_movie, n_recommendations)
                
                if recommendations:
                    st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 Movies similar to **{selected_movie}**")
                    
                    for i, rec in enumerate(recommendations, 1):
                        # Get movie_id from the processed_df using title
                        movie_id = recommender.processed_df[recommender.processed_df['title'] == rec['title']]['movie_id'].iloc[0]
                        poster_url = fetch_poster(movie_id)
                        display_movie_card(rec, poster_url, {'similarity_score': rec['similarity_score']})
                        st.divider()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("No recommendations found for this movie.")
    
    elif mode == "👥 Collaborative Filtering":
        st.markdown('<h2 class="sub-header">👥 Collaborative Filtering Recommendations</h2>', unsafe_allow_html=True)
        st.markdown("Get personalized recommendations based on user behavior patterns (simulated user data).")
        
        # User selection
        user_id = st.selectbox(
            "Select a user ID (simulated):",
            range(1000),
            index=0
        )
        
        # Number of recommendations
        n_recommendations = st.slider("Number of recommendations:", 3, 10, 5)
        
        if st.button("👥 Get Collaborative Recommendations", type="primary"):
            with st.spinner("Finding personalized recommendations..."):
                recommendations = recommender.get_collaborative_recommendations(user_id, n_recommendations)
                
                if recommendations:
                    st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
                    st.markdown(f"### 👤 Personalized recommendations for User {user_id}")
                    
                    for i, rec in enumerate(recommendations, 1):
                        # Get movie_id from the processed_df using title
                        movie_id = recommender.processed_df[recommender.processed_df['title'] == rec['title']]['movie_id'].iloc[0]
                        poster_url = fetch_poster(movie_id)
                        display_movie_card(rec, poster_url, {'predicted_rating': rec['predicted_rating']})
                        st.divider()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("No recommendations found for this user.")
    
    elif mode == "🚀 Hybrid":
        st.markdown('<h2 class="sub-header">🚀 Hybrid Recommendations</h2>', unsafe_allow_html=True)
        st.markdown("Get the best of both worlds by combining content-based and collaborative filtering approaches.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            movie_list = recommender.processed_df['title'].values.tolist()
            # Find default index safely
            default_index = 0
            try:
                if "Spider-Man" in movie_list:
                    default_index = movie_list.index("Spider-Man")
            except:
                default_index = 0
                
            selected_movie = st.selectbox(
                'Select a movie:',
                movie_list,
                index=default_index
            )
        
        with col2:
            user_id = st.selectbox(
                "Select a user ID:",
                range(1000),
                index=0
            )
        
        # Number of recommendations
        n_recommendations = st.slider("Number of recommendations:", 3, 15, 8)
        
        if st.button("🚀 Get Hybrid Recommendations", type="primary"):
            with st.spinner("Combining recommendation approaches..."):
                recommendations = recommender.get_hybrid_recommendations(
                    movie_title=selected_movie,
                    user_id=user_id,
                    n_recommendations=n_recommendations
                )
                
                if recommendations:
                    st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
                    st.markdown(f"### 🚀 Hybrid recommendations for **{selected_movie}** + User {user_id}")
                    
                    for i, rec in enumerate(recommendations, 1):
                        # Get movie_id from the processed_df using title
                        movie_id = recommender.processed_df[recommender.processed_df['title'] == rec['title']]['movie_id'].iloc[0]
                        poster_url = fetch_poster(movie_id)
                        score_info = {}
                        if 'similarity_score' in rec:
                            score_info['similarity_score'] = rec['similarity_score']
                        elif 'predicted_rating' in rec:
                            score_info['predicted_rating'] = rec['predicted_rating']
                        
                        display_movie_card(rec, poster_url, score_info)
                        st.divider()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("No hybrid recommendations found.")
    
    elif mode == "📊 System Info":
        st.markdown('<h2 class="sub-header">📊 System Information</h2>', unsafe_allow_html=True)
        
        # System statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Movies", len(recommender.processed_df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Simulated Users", recommender.user_movie_matrix.shape[0])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("User-Movie Matrix", f"{recommender.user_movie_matrix.shape[0]} × {recommender.user_movie_matrix.shape[1]}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("SVD Components", recommender.svd_model.n_components)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Data sample
        st.markdown("### 📋 Sample Movie Data")
        sample_data = recommender.processed_df[['title', 'genres', 'vote_average', 'popularity']].head(10)
        st.dataframe(sample_data, use_container_width=True)
        
        # Model information
        st.markdown("### 🔧 Model Details")
        st.markdown("""
        - **Content-Based Model**: TF-IDF vectorization with cosine similarity
        - **Collaborative Filtering**: SVD-based matrix factorization
        - **Hybrid Approach**: Combines both methods for optimal recommendations
        - **Text Processing**: Advanced NLP with stemming and stop word removal
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border-radius: 16px; border: 1px solid #e5e7eb; margin-top: 3rem;'>
        <div style='font-size: 1.5rem; font-weight: 600; color: #6366f1; margin-bottom: 1rem;'>🎬 Hybrid Movie Recommender</div>
        <p style='color: #6b7280; margin-bottom: 0.5rem;'>Built with Streamlit • Powered by Machine Learning • Data from TMDB</p>
        <p style='color: #9ca3af; font-size: 0.9rem;'>A sophisticated recommendation system demonstrating content-based and collaborative filtering approaches</p>
        <div style='margin-top: 1rem;'>
            <span style='display: inline-block; padding: 0.5rem 1rem; background: linear-gradient(135deg, #6366f1 0%, #10b981 100%); color: white; border-radius: 8px; font-size: 0.9rem; font-weight: 500;'>🚀 Production Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
