#!/usr/bin/env python3
"""
MBU Weather Intelligence - Quick Setup
=====================================
Complete setup script for the weather prediction system
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def train_models():
    """Train all ML models"""
    print("🤖 Training ML models...")
    try:
        subprocess.check_call([sys.executable, "train_models.py"])
        print("✅ All models trained successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error training models: {e}")
        return False

def check_data_file():
    """Check if data.csv exists"""
    if not os.path.exists('data.csv'):
        print("❌ data.csv not found!")
        print("Please ensure data.csv is in the current directory.")
        return False
    print("✅ data.csv found!")
    return True

def main():
    print("🌤️ MBU Weather Intelligence - Quick Setup")
    print("=" * 60)
    
    # Check data file
    if not check_data_file():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Train models
    if not train_models():
        return
    
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("🚀 Ready to run the application!")
    print("Run: streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    main()