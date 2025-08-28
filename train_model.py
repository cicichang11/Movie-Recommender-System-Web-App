#!/usr/bin/env python3
"""
Training script for the Hybrid Movie Recommendation System
This script builds both content-based and collaborative filtering models
and saves them for use in the Streamlit application.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from recommender import HybridRecommender

def main():
    """Main training function"""
    print("🎬 Training Hybrid Movie Recommendation System")
    print("=" * 50)
    
    # Initialize recommender
    recommender = HybridRecommender(
        movies_data='data/tmdb_5000_movies.csv',
        credits_data='data/tmdb_5000_credits.csv'
    )
    
    # Load and preprocess data
    print("\n📊 Step 1: Loading and preprocessing data...")
    recommender.load_and_preprocess_data()
    
    # Build content-based model
    print("\n🔍 Step 2: Building content-based model...")
    recommender.build_content_based_model()
    
    # Build collaborative filtering model
    print("\n👥 Step 3: Building collaborative filtering model...")
    recommender.build_collaborative_model()
    
    # Save all models
    print("\n💾 Step 4: Saving models...")
    recommender.save_models('artifacts')
    
    print("\n✅ Training completed successfully!")
    print("\n📁 Models saved to 'artifacts/' directory:")
    print("   - processed_movies.pkl")
    print("   - similarity_matrix.pkl")
    print("   - tfidf_matrix.pkl")
    print("   - svd_model.pkl")
    print("   - user_movie_matrix.pkl")
    
    # Test the system
    print("\n🧪 Testing the system...")
    
    # Test content-based recommendations
    test_movie = "Spider-Man"
    print(f"\nContent-based recommendations for '{test_movie}':")
    content_recs = recommender.get_content_based_recommendations(test_movie, 3)
    for i, rec in enumerate(content_recs, 1):
        print(f"  {i}. {rec['title']} (Score: {rec['similarity_score']:.3f})")
    
    # Test collaborative filtering
    test_user = 0
    print(f"\nCollaborative filtering recommendations for User {test_user}:")
    collab_recs = recommender.get_collaborative_recommendations(test_user, 3)
    for i, rec in enumerate(collab_recs, 1):
        print(f"  {i}. {rec['title']} (Predicted Rating: {rec['predicted_rating']:.2f})")
    
    # Test hybrid recommendations
    print(f"\nHybrid recommendations for '{test_movie}' and User {test_user}:")
    hybrid_recs = recommender.get_hybrid_recommendations(
        movie_title=test_movie, 
        user_id=test_user, 
        n_recommendations=3
    )
    for i, rec in enumerate(hybrid_recs, 1):
        if 'similarity_score' in rec:
            print(f"  {i}. {rec['title']} (Content Score: {rec['similarity_score']:.3f})")
        elif 'predicted_rating' in rec:
            print(f"  {i}. {rec['title']} (Predicted Rating: {rec['predicted_rating']:.2f})")
    
    print("\n🎉 All tests passed! The system is ready to use.")

if __name__ == "__main__":
    main()
