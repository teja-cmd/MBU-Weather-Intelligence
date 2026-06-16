#!/usr/bin/env python3
"""
MBU Weather Intelligence - Streamlit Cloud Entry Point
====================================================
Optimized entry point for Streamlit Cloud deployment
"""

import os
import sys
import streamlit as st

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
try:
    from app import *
    
    # Initialize the application
    if __name__ == "__main__":
        # This runs when deployed on Streamlit Cloud
        pass
        
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.info("Please ensure all required packages are installed.")
except Exception as e:
    st.error(f"Application Error: {e}")
    st.info("There was an error loading the application. Please try refreshing the page.")