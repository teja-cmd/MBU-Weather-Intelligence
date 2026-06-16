#!/usr/bin/env python3
"""
MBU Weather Intelligence - Quick Start
=====================================
One-click startup script for the weather prediction system
"""

import os
import sys
import subprocess
import time

def check_models():
    """Check if models are trained"""
    models_dir = 'models'
    if not os.path.exists(models_dir):
        return False
    
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
    return len(model_files) >= 70  # Should have 70+ model files

def main():
    print("🌤️ MBU Weather Intelligence - Quick Start")
    print("=" * 50)
    
    # Check if models exist
    if not check_models():
        print("⚠️  Models not found. Training models first...")
        print("📊 This may take a few minutes...")
        
        try:
            result = subprocess.run([sys.executable, 'train_models.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Models trained successfully!")
            else:
                print("❌ Error training models:")
                print(result.stderr)
                return
        except Exception as e:
            print(f"❌ Error: {e}")
            return
    else:
        print("✅ Models found and ready!")
    
    print("\n🚀 Starting Streamlit app...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Shutting down MBU Weather Intelligence...")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == "__main__":
    main()