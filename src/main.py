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
import logging
from datetime import datetime
import socket


def setup_logging():
    """
    Configure logging to both file and console.
    Logs are saved to 'app.log' in the current directory.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"rfactor_app_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger


def get_base_dir():
    """
    Get the base directory of the application.
    Works both in development and when frozen with PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        # Use the directory where the executable is located, not _MEIPASS
        return Path(sys.executable).parent
    else:
        # Running in development
        return Path(__file__).resolve().parent.parent


def is_port_in_use(port, host='127.0.0.1'):
    """
    Check if a port is already in use.

    Args:
        port: Port number to check
        host: Host address to check (default: 127.0.0.1)

    Returns:
        bool: True if port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True


def find_free_port(start_port=5000, max_attempts=10):
    """
    Find a free port starting from start_port.

    Args:
        start_port: Port to start checking from
        max_attempts: Maximum number of ports to try

    Returns:
        int: Free port number, or None if no free port found
    """
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return None


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

    # Initialize logging first
    logger = setup_logging()

    try:
        # Set the base directory
        base_dir = get_base_dir()
        logger.info(f"Base directory: {base_dir}")
        logger.info(f"Frozen: {getattr(sys, 'frozen', False)}")

        os.chdir(base_dir)
        logger.info(f"Working directory: {os.getcwd()}")

        # Check if config.json exists
        config_path = base_dir / "config.json"
        if not config_path.exists():
            error_msg = "config.json not found!"
            logger.error(error_msg)
            print("WARNING: config.json not found!")
            print()
            print("Please create a config.json file with your rFactor installation path.")
            print("Example:")
            print('{')
            print('  "rfactor_path": "C:/Program Files (x86)/Steam/steamapps/common/rFactor"')
            print('}')
            print()
            input("Press Enter to exit...")
            sys.exit(1)

        logger.info(f"Config file found: {config_path}")

        # Configuration
        host = "127.0.0.1"
        port = 5000

        # Check if port is available
        if is_port_in_use(port, host):
            logger.warning(f"Port {port} is already in use!")
            print(f"WARNING: Port {port} is already in use by another application.")
            print()

            # Try to find a free port
            free_port = find_free_port(port + 1, max_attempts=10)
            if free_port:
                print(f"Using alternative port: {free_port}")
                logger.info(f"Using alternative port: {free_port}")
                port = free_port
            else:
                error_msg = f"Could not find a free port between {port} and {port + 10}"
                logger.error(error_msg)
                print()
                print("ERROR: Could not find an available port to start the server.")
                print()
                print("Suggestions:")
                print(f"  - Close any application using port {port}")
                print("  - Or restart your computer to free up ports")
                print()
                input("Press Enter to exit...")
                sys.exit(1)

        print(f"Starting server on http://{host}:{port}")
        print()
        print("Application URLs:")
        print(f"   Frontend:  http://localhost:{port}/")
        print(f"   API Docs:  http://localhost:{port}/api/docs")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 70)
        print()

        logger.info(f"Starting server on {host}:{port}")

        # Start browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, args=(port, 3))
        browser_thread.daemon = True
        browser_thread.start()

        # Import the app here to ensure proper path resolution
        if getattr(sys, 'frozen', False):
            # When frozen, add the _internal directory to path
            internal_dir = Path(sys._MEIPASS)
            logger.info(f"Adding to sys.path: {internal_dir}")
            if str(internal_dir) not in sys.path:
                sys.path.insert(0, str(internal_dir))

        # Import the app
        from src.web.app import app

        logger.info("App imported successfully")

        # Start the server
        uvicorn.run(
            app,  # Pass the app object directly instead of string
            host=host,
            port=port,
            log_level="info",
            access_log=True,
        )

    except KeyboardInterrupt:
        logger.info("Server stopped by user (Ctrl+C)")
        print("\n\nShutting down server...")
        print("Goodbye!")
        time.sleep(1)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"\n\nFATAL ERROR: {e}")
        print(f"\nFull error details have been logged to: logs/")
        print("\nPlease check:")
        print("  - config.json is properly configured")
        print("  - All required files are present")
        print("\nCheck the log file for detailed error information.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    finally:
        # Always wait before closing if running as executable
        if getattr(sys, 'frozen', False):
            time.sleep(0.5)


if __name__ == "__main__":
    main()
