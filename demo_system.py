#!/usr/bin/env python3
"""
Demo script for the Hybrid Movie Recommendation System
This script demonstrates the system's capabilities without requiring the Streamlit interface.
"""

import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from recommender import HybridRecommender

def print_header():
    """Print a beautiful header"""
    print("🎬" * 50)
    print("🎬           HYBRID MOVIE RECOMMENDER DEMO           🎬")
    print("🎬" * 50)
    print()

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def demo_content_based(recommender):
    """Demonstrate content-based recommendations"""
    print_section("CONTENT-BASED RECOMMENDATIONS")
    
    test_movies = ["Spider-Man", "The Dark Knight", "Inception", "Pulp Fiction"]
    
    for movie in test_movies:
        if movie in recommender.processed_df['title'].values:
            print(f"\n🎭 Finding movies similar to: {movie}")
            recommendations = recommender.get_content_based_recommendations(movie, 3)
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec['title']}")
                    print(f"     Genres: {', '.join(rec['genres'][:3])}")
                    print(f"     Similarity: {rec['similarity_score']:.3f}")
                    print(f"     Rating: ⭐ {rec['vote_average']:.1f}/10")
                    print()
            else:
                print(f"  ❌ No recommendations found for {movie}")
        else:
            print(f"  ❌ Movie '{movie}' not found in dataset")

def demo_collaborative(recommender):
    """Demonstrate collaborative filtering recommendations"""
    print_section("COLLABORATIVE FILTERING RECOMMENDATIONS")
    
    test_users = [0, 100, 500, 999]
    
    for user_id in test_users:
        print(f"\n👤 Personalized recommendations for User {user_id}:")
        recommendations = recommender.get_collaborative_recommendations(user_id, 3)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec['title']}")
                print(f"     Genres: {', '.join(rec['genres'][:3])}")
                print(f"     Predicted Rating: {rec['predicted_rating']:.2f}/5.0")
                print(f"     TMDB Rating: ⭐ {rec['vote_average']:.1f}/10")
                print()
        else:
            print(f"  ❌ No recommendations found for User {user_id}")

def demo_hybrid(recommender):
    """Demonstrate hybrid recommendations"""
    print_section("HYBRID RECOMMENDATIONS")
    
    test_cases = [
        ("Spider-Man", 0),
        ("The Dark Knight", 100),
        ("Inception", 500)
    ]
    
    for movie, user_id in test_cases:
        if movie in recommender.processed_df['title'].values:
            print(f"\n🚀 Hybrid recommendations for '{movie}' + User {user_id}:")
            recommendations = recommender.get_hybrid_recommendations(
                movie_title=movie,
                user_id=user_id,
                n_recommendations=4
            )
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec['title']}")
                    print(f"     Genres: {', '.join(rec['genres'][:3])}")
                    
                    if 'similarity_score' in rec:
                        print(f"     Content Score: {rec['similarity_score']:.3f}")
                    elif 'predicted_rating' in rec:
                        print(f"     Predicted Rating: {rec['predicted_rating']:.2f}/5.0")
                    
                    print(f"     TMDB Rating: ⭐ {rec['vote_average']:.1f}/10")
                    print()
            else:
                print(f"  ❌ No hybrid recommendations found")
        else:
            print(f"  ❌ Movie '{movie}' not found in dataset")

def demo_system_info(recommender):
    """Display system information"""
    print_section("SYSTEM INFORMATION")
    
    print(f"📊 Dataset Statistics:")
    print(f"  • Total Movies: {len(recommender.processed_df):,}")
    print(f"  • Simulated Users: {recommender.user_movie_matrix.shape[0]:,}")
    print(f"  • User-Movie Matrix: {recommender.user_movie_matrix.shape[0]:,} × {recommender.user_movie_matrix.shape[1]:,}")
    print(f"  • SVD Components: {recommender.svd_model.n_components}")
    
    print(f"\n🎭 Content-Based Model:")
    print(f"  • TF-IDF Matrix Shape: {recommender.tfidf_matrix.shape}")
    print(f"  • Similarity Matrix Shape: {recommender.similarity_matrix.shape}")
    
    print(f"\n👥 Collaborative Filtering Model:")
    print(f"  • SVD Explained Variance: {sum(recommender.svd_model.explained_variance_ratio_):.3f}")
    print(f"  • Top 5 Components Variance: {sum(recommender.svd_model.explained_variance_ratio_[:5]):.3f}")
    
    print(f"\n📈 Sample Movie Data:")
    sample_movies = recommender.processed_df[['title', 'genres', 'vote_average', 'popularity']].head(5)
    for _, movie in sample_movies.iterrows():
        genres = ', '.join(movie['genres'][:2]) if movie['genres'] else 'N/A'
        print(f"  • {movie['title']} | {genres} | ⭐ {movie['vote_average']:.1f} | 📊 {movie['popularity']:.1f}")

def performance_test(recommender):
    """Test system performance"""
    print_section("PERFORMANCE TEST")
    
    print("⏱️ Testing recommendation speed...")
    
    # Test content-based
    start_time = time.time()
    content_recs = recommender.get_content_based_recommendations("Spider-Man", 5)
    content_time = time.time() - start_time
    
    # Test collaborative
    start_time = time.time()
    collab_recs = recommender.get_collaborative_recommendations(0, 5)
    collab_time = time.time() - start_time
    
    # Test hybrid
    start_time = time.time()
    hybrid_recs = recommender.get_hybrid_recommendations("Spider-Man", 0, 5)
    hybrid_time = time.time() - start_time
    
    print(f"🎭 Content-Based: {content_time:.3f}s")
    print(f"👥 Collaborative: {collab_time:.3f}s")
    print(f"🚀 Hybrid: {hybrid_time:.3f}s")
    print(f"📊 Total Recommendations Generated: {len(content_recs) + len(collab_recs) + len(hybrid_recs)}")

def main():
    """Main demo function"""
    print_header()
    
    print("🔧 Loading the recommendation system...")
    
    try:
        # Initialize recommender
        recommender = HybridRecommender(
            movies_data='data/tmdb_5000_movies.csv',
            credits_data='data/tmdb_5000_credits.csv'
        )
        
        # Try to load pre-trained models
        if not recommender.load_models('artifacts'):
            print("❌ Pre-trained models not found. Please run 'python train_model.py' first.")
            print("\n💡 This demo requires trained models. Please:")
            print("   1. Run: python train_model.py")
            print("   2. Then run: python demo_system.py")
            return
        
        print("✅ Models loaded successfully!")
        print(f"📊 Ready to recommend from {len(recommender.processed_df):,} movies")
        
        # Run demos
        demo_content_based(recommender)
        demo_collaborative(recommender)
        demo_hybrid(recommender)
        demo_system_info(recommender)
        performance_test(recommender)
        
        print_section("DEMO COMPLETED")
        print("🎉 All demos completed successfully!")
        print("\n🚀 Ready to run the full Streamlit app:")
        print("   streamlit run app_improved.py")
        
    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure all dependencies are installed")
        print("   2. Run: python train_model.py")
        print("   3. Check that data files exist in data/ directory")

if __name__ == "__main__":
    main()
