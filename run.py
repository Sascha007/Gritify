#!/usr/bin/env python3
"""
Gritify - Gridfinity Structure Generator
Run this script to start the web application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import HOST, PORT, DEBUG

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║        Gritify - Starting Server...        ║
    ╚════════════════════════════════════════════╝
    
    🔲 Gridfinity Structure Generator
    
    Server starting at:
    🌐 http://localhost:5000
    
    Press Ctrl+C to stop the server
    """)
    
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
