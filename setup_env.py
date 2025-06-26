#!/usr/bin/env python3
"""
Setup script for Voice Chat AI Application
Creates .env file with OpenAI API key
"""

import os

def create_env_file():
    """Create .env file with OpenAI API key."""
    env_path = '.env'
    
    if os.path.exists(env_path):
        print("❗ .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    print("🔑 Setting up your OpenAI API key...")
    print("Get your API key from: https://platform.openai.com/api-keys")
    print()
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: OpenAI API keys usually start with 'sk-'")
        proceed = input("Continue anyway? (y/n): ").lower().strip()
        if proceed != 'y':
            print("Setup cancelled.")
            return
    
    # Create .env file
    env_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Voice Chat AI Application
# This file contains sensitive information - never commit to version control!
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print(f"📁 Created: {os.path.abspath(env_path)}")
        print()
        print("🚀 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the server: python manage.py runserver")
        print("3. Open http://127.0.0.1:8000/ in your browser")
        print()
        print("🔒 Security reminder: Never commit your .env file to version control!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    print("🎙️ Voice Chat AI - Environment Setup")
    print("=" * 50)
    create_env_file() 