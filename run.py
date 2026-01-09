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
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped. Goodbye!")
