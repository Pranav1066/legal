"""
Quick Start Script for Legal Intelligence System
Launches web interface directly
"""
import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config

if __name__ == "__main__":
    print(f"Starting {config.APP_NAME}...")
    print(f"Web interface will open at: http://localhost:{config.WEB_PORT}")
    print("\nPress Ctrl+C to stop the server\n")

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "web_interface.py",
            "--server.port", str(config.WEB_PORT),
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure Streamlit is installed: pip install streamlit")
