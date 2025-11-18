"""
Main Entry Point for Legal Intelligence System
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from utils.logger import setup_logger
from utils.database import db

logger = setup_logger('main')


def print_banner():
    """Print system banner"""
    print("=" * 70)
    print(f"  {config.APP_NAME}")
    print(f"  Version {config.APP_VERSION}")
    print("=" * 70)
    print()


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 70)
    print("  MAIN MENU")
    print("=" * 70)
    print()
    print("  1. Launch Web Interface (Streamlit)")
    print("  2. Launch API Server (FastAPI)")
    print("  3. Launch CLI Interface")
    print("  4. View System Status")
    print("  5. Run Database Setup")
    print("  6. View Configuration")
    print("  0. Exit")
    print()


def view_status():
    """View system status"""
    print("\n" + "=" * 70)
    print("  SYSTEM STATUS")
    print("=" * 70)
    print()

    try:
        # Database stats
        stats = db.get_database_stats()
        print("Database Statistics:")
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

        # Configuration
        print(f"\nConfiguration:")
        print(f"  AI Model: {config.AI_MODEL}")
        print(f"  Web Port: {config.WEB_PORT}")
        print(f"  API Port: {config.API_PORT}")
        print(f"  Database: {config.DATABASE_PATH}")
        print(f"  Log Level: {config.LOG_LEVEL}")

        print("\n✓ System operational")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def view_configuration():
    """View configuration"""
    print("\n" + "=" * 70)
    print("  CONFIGURATION")
    print("=" * 70)
    print()

    config_summary = config.get_config_summary()
    for key, value in config_summary.items():
        if isinstance(value, dict):
            print(f"\n{key.replace('_', ' ').title()}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    # Validate configuration
    issues = config.validate_config()
    if issues:
        print("\n⚠ Configuration Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✓ Configuration valid")


def setup_database():
    """Setup database"""
    print("\n" + "=" * 70)
    print("  DATABASE SETUP")
    print("=" * 70)
    print()

    try:
        print("Initializing database schema...")
        # Database is auto-initialized on import, but we can verify
        stats = db.get_database_stats()
        print(f"✓ Database initialized successfully")
        print(f"  Location: {config.DATABASE_PATH}")
        print(f"  Tables: {len(stats)}")
        print("\nDatabase is ready to use!")

    except Exception as e:
        print(f"✗ Error: {str(e)}")


def launch_web():
    """Launch web interface"""
    print("\nLaunching web interface...")
    print(f"Starting Streamlit on port {config.WEB_PORT}...")
    print(f"\nAccess the web interface at: http://localhost:{config.WEB_PORT}")
    print("\nPress Ctrl+C to stop the server\n")

    try:
        import subprocess
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "web_interface.py",
            "--server.port", str(config.WEB_PORT),
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\nWeb server stopped")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nTry running manually: streamlit run web_interface.py")


def launch_api():
    """Launch API server"""
    print("\nLaunching API server...")
    print(f"Starting FastAPI on port {config.API_PORT}...")
    print(f"\nAccess the API at: http://localhost:{config.API_PORT}")
    print(f"API Documentation: http://localhost:{config.API_PORT}/docs")
    print("\nPress Ctrl+C to stop the server\n")

    try:
        from api_server import run_server
        run_server()
    except KeyboardInterrupt:
        print("\n\nAPI server stopped")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def launch_cli():
    """Launch CLI interface"""
    print("\nLaunching CLI interface...")
    print("Type 'python cli_interface.py --help' for available commands\n")

    try:
        import subprocess
        subprocess.run([sys.executable, "cli_interface.py", "--help"])
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def main():
    """Main application loop"""
    print_banner()

    logger.info("Legal Intelligence System starting...")

    # Validate configuration
    issues = config.validate_config()
    if issues:
        print("⚠ Configuration Issues Detected:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease fix these issues in your .env file before proceeding.")
        print()

    while True:
        print_menu()

        try:
            choice = input("Enter your choice (0-6): ").strip()

            if choice == '0':
                print("\nThank you for using Legal Intelligence System!")
                logger.info("System shutdown")
                sys.exit(0)

            elif choice == '1':
                launch_web()

            elif choice == '2':
                launch_api()

            elif choice == '3':
                launch_cli()

            elif choice == '4':
                view_status()

            elif choice == '5':
                setup_database()

            elif choice == '6':
                view_configuration()

            else:
                print("\n✗ Invalid choice. Please select 0-6.")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            logger.info("System shutdown (KeyboardInterrupt)")
            sys.exit(0)

        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}", exc_info=True)
            print(f"\n✗ Error: {str(e)}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
