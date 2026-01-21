"""
One-time setup script for Text Simplifier
Run this once: python setup.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║         TEXT SIMPLIFIER - ONE-TIME SETUP                   ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Install Python packages
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python packages"
    ):
        print("\n⚠️  Warning: Package installation had issues")
        print("Try running manually: pip install -r requirements.txt")
    
    # Step 2: Download spaCy model
    if not run_command(
        "python -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    ):
        print("\n⚠️  Warning: spaCy model download had issues")
        print("Try running manually: python -m spacy download en_core_web_sm")
    
    # Step 3: Check for .env file
    print(f"\n{'='*60}")
    print("🔑 Checking API Key Configuration")
    print(f"{'='*60}")
    
    if os.path.exists('.env'):
        print("✓ .env file found")
        with open('.env', 'r') as f:
            content = f.read()
            if 'HUGGINGFACE_API_KEY' in content:
                print("✓ HUGGINGFACE_API_KEY configured")
            else:
                print("⚠️  .env file exists but missing HUGGINGFACE_API_KEY")
                print("   Add this line to .env:")
                print("   HUGGINGFACE_API_KEY=your_key_here")
    else:
        print("ℹ️  No .env file found")
        print("   Module will run in DEMO MODE")
        print("\n   To enable full functionality:")
        print("   1. Create a file named '.env' in this folder")
        print("   2. Add: HUGGINGFACE_API_KEY=your_huggingface_key")
        
        # Ask if user wants to create .env now
        create_env = input("\n   Create .env file now? (y/n): ").lower().strip()
        if create_env == 'y':
            api_key = input("   Enter your Hugging Face API key: ").strip()
            with open('.env', 'w') as f:
                f.write(f"HUGGINGFACE_API_KEY={api_key}\n")
            print("   ✓ .env file created")
    
    # Final message
    print(f"\n{'='*60}")
    print("🎉 SETUP COMPLETE!")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("1. Run: python test_standalone.py")
    print("2. Check results")
    print("\nIf you encounter issues, check TEAMMATE_INSTRUCTIONS.md")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
