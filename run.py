#!/usr/bin/env python3
"""
Gritify - Gridfinity Structure Generator
Run this script to start the web application
"""

import sys
import os
import multiprocessing

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Fix for macOS multiprocessing with Flask reloader
    multiprocessing.freeze_support()
    
    from app import app
    from config import HOST, PORT, DEBUG
    
    print("""
    ╔════════════════════════════════════════════╗
    ║        Gritify - Starting Server...        ║
    ╚════════════════════════════════════════════╝
    
    🔲 Gridfinity Structure Generator
    
    Server starting at:
    🌐 http://localhost:5020
    
    Press Ctrl+C to stop the server
    """)
    
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
