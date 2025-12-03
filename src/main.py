"""
Main entry point for the rFactor Championship Creator application.

This module serves as the executable entry point when the application is packaged.
It starts the web server and opens the browser automatically.
"""

import sys
import os
import webbrowser
import time
from pathlib import Path
import threading
import uvicorn


def get_base_dir():
    """
    Get the base directory of the application.
    Works both in development and when frozen with PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys._MEIPASS)
    else:
        # Running in development
        return Path(__file__).resolve().parent.parent


def open_browser(port=5000, delay=3):
    """
    Open the default web browser after a delay.

    Args:
        port: Port number where the server is running
        delay: Seconds to wait before opening browser
    """
    time.sleep(delay)
    url = f"http://localhost:{port}"
    print(f"\nOpening browser at {url}...")
    webbrowser.open(url)


def main():
    """Main entry point for the application."""
    print("=" * 70)
    print("    rFactor Championship Creator")
    print("=" * 70)
    print()

    # Set the base directory
    base_dir = get_base_dir()
    os.chdir(base_dir)

    # Check if config.json exists
    config_path = base_dir / "config.json"
    if not config_path.exists():
        print("⚠️  WARNING: config.json not found!")
        print()
        print("Please create a config.json file with your rFactor installation path.")
        print("Example:")
        print('{')
        print('  "rfactor_path": "C:/Program Files (x86)/Steam/steamapps/common/rFactor"')
        print('}')
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    # Configuration
    host = "127.0.0.1"
    port = 5000

    print(f"Starting server on http://{host}:{port}")
    print()
    print("📋 Application URLs:")
    print(f"   Frontend:  http://localhost:{port}/")
    print(f"   API Docs:  http://localhost:{port}/api/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()

    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(port, 3))
    browser_thread.daemon = True
    browser_thread.start()

    # Start the server
    try:
        uvicorn.run(
            "src.web.app:app",
            host=host,
            port=port,
            log_level="info",
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        print("Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error starting server: {e}")
        print("\nPlease check:")
        print(f"  - Port {port} is not already in use")
        print("  - config.json is properly configured")
        print("  - All required files are present")
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
