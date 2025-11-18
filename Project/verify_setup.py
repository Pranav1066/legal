"""
Verify Legal Intelligence System Setup
Run this script to check if everything is configured correctly
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Use ASCII-compatible symbols for Windows
OK = "[OK]"
FAIL = "[X]"
WARN = "[!]"

print("=" * 70)
print("  Legal Intelligence System - Setup Verification")
print("=" * 70)
print()

# Test 1: Check Python version
print("1. Checking Python version...")
if sys.version_info < (3, 8):
    print(f"   {FAIL} Python 3.8+ required. You have: {sys.version}")
    sys.exit(1)
else:
    print(f"   {OK} Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Test 2: Check imports
print("\n2. Checking required imports...")
required_modules = [
    ('agno', 'Agno framework'),
    ('streamlit', 'Web interface'),
    ('fastapi', 'API server'),
    ('click', 'CLI tool'),
    ('pydantic', 'Data validation'),
    ('google.generativeai', 'Gemini AI')
]

missing_modules = []
for module, description in required_modules:
    try:
        __import__(module)
        print(f"   {OK} {module} ({description})")
    except ImportError:
        print(f"   {FAIL} {module} ({description}) - NOT INSTALLED")
        missing_modules.append(module)

if missing_modules:
    print(f"\n   Install missing modules: pip install {' '.join(missing_modules)}")
    sys.exit(1)

# Test 3: Check configuration
print("\n3. Checking configuration...")
try:
    from config import config

    # Check API key
    if not config.GEMINI_API_KEY:
        print(f"   {FAIL} GEMINI_API_KEY not set in .env file")
        print("   -> Create .env file and add: GEMINI_API_KEY=your_key_here")
        print("   -> Get your key at: https://ai.google.dev/")
        sys.exit(1)
    elif config.GEMINI_API_KEY == "your_gemini_api_key_here" or len(config.GEMINI_API_KEY) < 20:
        print(f"   {FAIL} GEMINI_API_KEY looks invalid (placeholder or too short)")
        print("   -> Update .env with your actual API key from https://ai.google.dev/")
        sys.exit(1)
    else:
        print(f"   {OK} GEMINI_API_KEY configured (length: {len(config.GEMINI_API_KEY)})")

    # Validate config
    issues = config.validate_config()
    if issues:
        print(f"   {WARN} Configuration issues found:")
        for issue in issues:
            print(f"     - {issue}")
    else:
        print(f"   {OK} Configuration valid")

    print(f"   {OK} AI Model: {config.AI_MODEL}")
    print(f"   {OK} Web Port: {config.WEB_PORT}")
    print(f"   {OK} API Port: {config.API_PORT}")

except Exception as e:
    print(f"   {FAIL} Configuration error: {str(e)}")
    sys.exit(1)

# Test 4: Check database
print("\n4. Checking database...")
try:
    from utils.database import db

    if Path(config.DATABASE_PATH).exists():
        stats = db.get_database_stats()
        print(f"   {OK} Database exists at: {config.DATABASE_PATH}")
        print(f"   {OK} Lawyers: {stats.get('lawyers_count', 0)}")
        print(f"   {OK} Cases: {stats.get('cases_count', 0)}")
        print(f"   {OK} Documents: {stats.get('legal_documents_count', 0)}")

        if stats.get('lawyers_count', 0) == 0:
            print(f"\n   {WARN} Database is empty. Run: python populate_sample_data.py")
    else:
        print(f"   {WARN} Database will be created at: {config.DATABASE_PATH}")
        print("   -> Run: python populate_sample_data.py to add sample data")

except Exception as e:
    print(f"   {FAIL} Database error: {str(e)}")
    sys.exit(1)

# Test 5: Test AI agent initialization
print("\n5. Testing AI agents...")
try:
    from agents.case_law_research_agent import case_law_agent
    print(f"   {OK} Case Law Research Agent initialized")

    from agents.contract_analysis_agent import contract_agent
    print(f"   {OK} Contract Analysis Agent initialized")

    from agents.compliance_advisory_agent import compliance_agent
    print(f"   {OK} Compliance Advisory Agent initialized")

    from agents.legal_drafting_agent import drafting_agent
    print(f"   {OK} Legal Drafting Agent initialized")

    from agents.litigation_strategy_agent import litigation_agent
    print(f"   {OK} Litigation Strategy Agent initialized")

except Exception as e:
    print(f"   {FAIL} Agent initialization error: {str(e)}")
    if "api_key" in str(e).lower():
        print("   -> Check your GEMINI_API_KEY in .env file")
    sys.exit(1)

# Test 6: Check logs directory
print("\n6. Checking logs directory...")
log_dir = Path(config.LOG_FILE).parent
if log_dir.exists():
    print(f"   {OK} Logs directory exists: {log_dir}")
else:
    print(f"   {WARN} Creating logs directory: {log_dir}")
    log_dir.mkdir(parents=True, exist_ok=True)

# Test 7: Port availability
print("\n7. Checking port availability...")
import socket

def is_port_available(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
            return True
    except OSError:
        return False

web_port_available = is_port_available(config.WEB_PORT)
api_port_available = is_port_available(config.API_PORT)

if web_port_available:
    print(f"   {OK} Web port {config.WEB_PORT} is available")
else:
    print(f"   {WARN} Web port {config.WEB_PORT} is in use (change WEB_PORT in .env)")

if api_port_available:
    print(f"   {OK} API port {config.API_PORT} is available")
else:
    print(f"   {WARN} API port {config.API_PORT} is in use (change API_PORT in .env)")

# Final summary
print("\n" + "=" * 70)
print("  VERIFICATION COMPLETE")
print("=" * 70)
print()

if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_gemini_api_key_here":
    print(f"{WARN} ACTION REQUIRED: Set your GEMINI_API_KEY in .env file")
    print()
elif stats.get('lawyers_count', 0) == 0:
    print(f"{WARN} RECOMMENDED: Run 'python populate_sample_data.py' to add sample data")
    print()
else:
    print(f"{OK} System is ready!")
    print()
    print("Next steps:")
    print("  1. Launch web interface: python start.py")
    print("  2. Launch API server: python api_server.py")
    print("  3. Use CLI: python cli_interface.py --help")
    print()

print("=" * 70)
