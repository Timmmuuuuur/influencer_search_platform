#!/usr/bin/env python3
"""
Setup Verification Script for Influencer Search Platform
This script checks if all required dependencies and configurations are in place.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node_version():
    """Check if Node.js is installed and version is 16 or higher"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip().lstrip('v')
            major_version = int(version.split('.')[0])
            if major_version >= 16:
                print(f"✅ Node.js {version} detected")
                return True
            else:
                print(f"❌ Node.js 16 or higher is required (found {version})")
                return False
        else:
            print("❌ Node.js is not installed")
            return False
    except FileNotFoundError:
        print("❌ Node.js is not installed")
        return False

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return False
    
    requirements_file = backend_path / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found in backend directory")
        return False
    
    print("✅ Backend requirements.txt found")
    return True

def check_frontend_dependencies():
    """Check if frontend dependencies are installed"""
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    package_json = frontend_path / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in frontend directory")
        return False
    
    print("✅ Frontend package.json found")
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ .env file not found in backend directory")
        print("   Please copy env.example to .env and fill in your API keys")
        return False
    
    required_keys = [
        "OPENAI_API_KEY",
        "YOUTUBE_API_KEY", 
        "EMAIL_USERNAME",
        "EMAIL_PASSWORD"
    ]
    
    missing_keys = []
    with open(env_file, 'r') as f:
        content = f.read()
        for key in required_keys:
            if f"{key}=" not in content or f"{key}=your_" in content:
                missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing or incomplete API keys: {', '.join(missing_keys)}")
        print("   Please update your .env file with valid API keys")
        return False
    
    print("✅ .env file configured with API keys")
    return True

def check_api_keys():
    """Test API key connectivity (optional)"""
    print("\n🔍 Testing API key connectivity...")
    
    # Test OpenAI API
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key and openai.api_key != "your_openai_api_key_here":
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not properly configured")
    except ImportError:
        print("⚠️  OpenAI package not installed (will be installed with requirements.txt)")
    
    # Test YouTube API
    try:
        from googleapiclient.discovery import build
        youtube_key = os.getenv("YOUTUBE_API_KEY")
        if youtube_key and youtube_key != "your_youtube_api_key_here":
            print("✅ YouTube API key configured")
        else:
            print("⚠️  YouTube API key not properly configured")
    except ImportError:
        print("⚠️  Google API package not installed (will be installed with requirements.txt)")

def main():
    """Main verification function"""
    print("🔍 Verifying Influencer Search Platform Setup...\n")
    
    checks = [
        check_python_version(),
        check_node_version(),
        check_backend_dependencies(),
        check_frontend_dependencies(),
        check_env_file()
    ]
    
    all_passed = all(checks)
    
    if all_passed:
        print("\n✅ All setup checks passed!")
        print("\n🚀 You're ready to start the platform:")
        print("   Run: ./start.sh (Mac/Linux) or start.bat (Windows)")
        print("   Or manually:")
        print("   1. cd backend && uvicorn app.main:app --reload")
        print("   2. cd frontend && npm run dev")
    else:
        print("\n❌ Some setup checks failed. Please fix the issues above before running the platform.")
        sys.exit(1)
    
    # Optional API key testing
    check_api_keys()

if __name__ == "__main__":
    main()
