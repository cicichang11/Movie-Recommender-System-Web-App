#!/usr/bin/env python3
"""
Setup script for Movie Recommender System
This script helps users set up the required data files and models.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path

def download_tmdb_data():
    """Download TMDB movie dataset"""
    print("📥 Downloading TMDB movie dataset...")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # URLs for TMDB data (you can replace these with actual URLs)
    tmdb_movies_url = "https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/download"
    tmdb_credits_url = "https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/download"
    
    print("⚠️  TMDB data files are large and not included in this repository.")
    print("📋 Please download the following files manually:")
    print("   1. tmdb_5000_movies.csv")
    print("   2. tmdb_5000_credits.csv")
    print("   📍 Place them in the 'data/' directory")
    print("   🔗 Download from: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")

def setup_models():
    """Setup or generate model files"""
    print("\n🤖 Setting up model files...")
    
    # Create artifacts directory
    os.makedirs("artifacts", exist_ok=True)
    
    print("⚠️  Model files are large and not included in this repository.")
    print("📋 You have two options:")
    print("   1. 🎯 Run 'python train_model.py' to generate models from scratch")
    print("   2. 📥 Download pre-trained models (if available)")
    print("   💡 Option 1 is recommended for first-time setup")

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'streamlit', 
        'plotly', 'requests', 'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print(f"   pip install {' '.join(missing_packages)}")
    else:
        print("✅ All required packages are installed!")

def main():
    """Main setup function"""
    print("🎬 Movie Recommender System - Setup")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Setup data
    download_tmdb_data()
    
    # Setup models
    setup_models()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("   1. 📁 Place TMDB CSV files in 'data/' directory")
    print("   2. 🚀 Run 'python train_model.py' to generate models")
    print("   3. 🌐 Run 'streamlit run app_improved.py' to start the app")
    print("\n📖 For more details, see README.md")

if __name__ == "__main__":
    main()
