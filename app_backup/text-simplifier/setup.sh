#!/bin/bash

# Text Simplifier Setup Script
# Automates the installation and configuration process

set -e  # Exit on error

echo "========================================="
echo "Text Simplifier - Setup Script"
echo "========================================="

# Check Python version
echo ""
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# Download spaCy model
echo ""
echo "📥 Downloading spaCy language model..."
python -m spacy download en_core_web_sm --quiet
echo "✓ spaCy model downloaded"

# Setup environment file
echo ""
echo "⚙️  Setting up environment configuration..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping..."
else
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Hugging Face token to .env"
    echo "   1. Get your token from: https://huggingface.co/settings/tokens"
    echo "   2. Edit .env file and replace 'your_huggingface_token_here' with your actual token"
fi

# Test installation
echo ""
echo "🧪 Testing installation..."
python -c "
from text_simplifier import TextSimplifier
from semantic_checker import SemanticChecker
from difficulty_scorer import DifficultyScorer
print('✓ All modules imported successfully')
"

echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "📝 Next Steps:"
echo "   1. Edit .env file and add your HF_TOKEN"
echo "   2. Activate virtual environment: source venv/bin/activate"
echo "   3. Run example: python example.py"
echo ""
echo "🔗 Get HF Token: https://huggingface.co/settings/tokens"
echo ""
