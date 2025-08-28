#!/bin/bash

echo "🎬 Setting up Hybrid Movie Recommendation System"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if data files exist
if [ ! -f "data/tmdb_5000_movies.csv" ] || [ ! -f "data/tmdb_5000_credits.csv" ]; then
    echo "❌ Data files not found in data/ directory"
    echo "Please ensure you have the TMDB dataset files:"
    echo "  - data/tmdb_5000_movies.csv"
    echo "  - data/tmdb_5000_credits.csv"
    exit 1
fi

echo "✅ Data files found"

# Create artifacts directory
mkdir -p artifacts

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Train the models: python train_model.py"
echo "2. Run the improved app: streamlit run app_improved.py"
echo "3. Or run the original app: streamlit run app.py"
echo ""
echo "Note: The first run of train_model.py may take several minutes to process the data."
echo ""
echo "Happy movie recommending! 🎬"
