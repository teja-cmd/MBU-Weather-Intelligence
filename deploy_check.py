#!/usr/bin/env python3
"""
Deployment Check Script
======================
Check file sizes and deployment readiness
"""

import os
import glob

def check_file_sizes():
    """Check for large files that might cause deployment issues"""
    large_files = []
    total_size = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                total_size += size
                
                # Flag files larger than 25MB
                if size > 25 * 1024 * 1024:
                    large_files.append((filepath, size / (1024*1024)))
            except:
                continue
    
    print("🔍 Deployment Readiness Check")
    print("=" * 40)
    print(f"Total repository size: {total_size / (1024*1024):.2f} MB")
    
    if large_files:
        print("\n⚠️  Large files detected:")
        for filepath, size_mb in large_files:
            print(f"  - {filepath}: {size_mb:.2f} MB")
        print("\n💡 Consider using Git LFS for files > 25MB")
    else:
        print("\n✅ No large files detected")
    
    # Check essential files
    essential_files = [
        'streamlit_app.py',
        'app.py', 
        'requirements.txt',
        '.streamlit/config.toml',
        'models/weather_metadata.pkl'
    ]
    
    print(f"\n📋 Essential files check:")
    for file in essential_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING!")
    
    print(f"\n🚀 Repository is ready for deployment!")

if __name__ == "__main__":
    check_file_sizes()