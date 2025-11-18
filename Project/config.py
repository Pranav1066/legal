"""
Configuration management for Legal Intelligence System
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class for Legal Intelligence System"""

    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "Legal Intelligence System")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Server Configuration
    WEB_PORT = int(os.getenv("WEB_PORT", "8501"))
    API_PORT = int(os.getenv("API_PORT", "8004"))
    CLI_ENABLED = os.getenv("CLI_ENABLED", "true").lower() == "true"

    # AI Model Configuration
    AI_MODEL = os.getenv("AI_MODEL", "gemini-2.5-flash-lite")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "8000"))

    # Database Configuration
    BASE_DIR = Path(__file__).parent
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "legal_intelligence.db"))
    ENABLE_DATABASE_LOGGING = os.getenv("ENABLE_DATABASE_LOGGING", "true").lower() == "true"

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "legal_intelligence.log"))
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "50"))
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # Legal Practice Areas
    DEFAULT_PRACTICE_AREAS = [
        area.strip()
        for area in os.getenv(
            "DEFAULT_PRACTICE_AREAS",
            "Corporate Law,Criminal Law,Civil Litigation,Intellectual Property,Employment Law,Tax Law,Real Estate,Family Law,Immigration Law,Environmental Law"
        ).split(",")
    ]

    # Jurisdiction Settings
    DEFAULT_JURISDICTIONS = [
        jurisdiction.strip()
        for jurisdiction in os.getenv(
            "DEFAULT_JURISDICTIONS",
            "Federal,State,Local,International"
        ).split(",")
    ]

    # Case Analysis Settings
    MIN_CASE_RELEVANCE_SCORE = float(os.getenv("MIN_CASE_RELEVANCE_SCORE", "0.6"))
    MAX_CASE_RECOMMENDATIONS = int(os.getenv("MAX_CASE_RECOMMENDATIONS", "20"))
    STATUTE_SEARCH_DEPTH = int(os.getenv("STATUTE_SEARCH_DEPTH", "50"))

    # Legal Research Metrics
    TARGET_CASE_SUCCESS_RATE = float(os.getenv("TARGET_CASE_SUCCESS_RATE", "0.75"))
    TARGET_COMPLIANCE_SCORE = float(os.getenv("TARGET_COMPLIANCE_SCORE", "0.95"))
    TARGET_DOCUMENT_ACCURACY = float(os.getenv("TARGET_DOCUMENT_ACCURACY", "0.99"))

    # Alert Thresholds
    DEADLINE_WARNING_DAYS = int(os.getenv("DEADLINE_WARNING_DAYS", "7"))
    CRITICAL_DEADLINE_DAYS = int(os.getenv("CRITICAL_DEADLINE_DAYS", "3"))
    HIGH_RISK_THRESHOLD = float(os.getenv("HIGH_RISK_THRESHOLD", "0.7"))
    COMPLIANCE_ALERT_THRESHOLD = float(os.getenv("COMPLIANCE_ALERT_THRESHOLD", "0.8"))

    # Document Analysis Settings
    ENABLE_CONTRACT_ANALYSIS = os.getenv("ENABLE_CONTRACT_ANALYSIS", "true").lower() == "true"
    ENABLE_RISK_ASSESSMENT = os.getenv("ENABLE_RISK_ASSESSMENT", "true").lower() == "true"
    ENABLE_PRECEDENT_SEARCH = os.getenv("ENABLE_PRECEDENT_SEARCH", "true").lower() == "true"
    ENABLE_COMPLIANCE_CHECK = os.getenv("ENABLE_COMPLIANCE_CHECK", "true").lower() == "true"
    ENABLE_LEGAL_DRAFTING = os.getenv("ENABLE_LEGAL_DRAFTING", "true").lower() == "true"

    # Contract Review Settings
    CONTRACT_RISK_CATEGORIES = [
        category.strip()
        for category in os.getenv(
            "CONTRACT_RISK_CATEGORIES",
            "Liability,Termination,Payment Terms,Intellectual Property,Confidentiality,Force Majeure,Indemnification,Warranties"
        ).split(",")
    ]

    # Compliance Framework Settings
    COMPLIANCE_FRAMEWORKS = [
        framework.strip()
        for framework in os.getenv(
            "COMPLIANCE_FRAMEWORKS",
            "GDPR,HIPAA,SOX,CCPA,PCI-DSS,ISO 27001,FCPA"
        ).split(",")
    ]

    # Cache Settings
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # Rate Limiting
    API_RATE_LIMIT_PER_MINUTE = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60"))
    WEB_SESSION_TIMEOUT_MINUTES = int(os.getenv("WEB_SESSION_TIMEOUT_MINUTES", "30"))

    # Feature Flags
    ENABLE_CASE_LAW_ANALYSIS = os.getenv("ENABLE_CASE_LAW_ANALYSIS", "true").lower() == "true"
    ENABLE_STATUTE_RESEARCH = os.getenv("ENABLE_STATUTE_RESEARCH", "true").lower() == "true"
    ENABLE_LEGAL_MEMO_GENERATION = os.getenv("ENABLE_LEGAL_MEMO_GENERATION", "true").lower() == "true"
    ENABLE_DUE_DILIGENCE = os.getenv("ENABLE_DUE_DILIGENCE", "true").lower() == "true"
    ENABLE_LITIGATION_PREDICTION = os.getenv("ENABLE_LITIGATION_PREDICTION", "true").lower() == "true"

    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            "app_name": cls.APP_NAME,
            "version": cls.APP_VERSION,
            "environment": cls.ENVIRONMENT,
            "web_port": cls.WEB_PORT,
            "api_port": cls.API_PORT,
            "ai_model": cls.AI_MODEL,
            "database_path": cls.DATABASE_PATH,
            "log_level": cls.LOG_LEVEL,
            "practice_areas": len(cls.DEFAULT_PRACTICE_AREAS),
            "jurisdictions": len(cls.DEFAULT_JURISDICTIONS),
            "features_enabled": {
                "case_law_analysis": cls.ENABLE_CASE_LAW_ANALYSIS,
                "statute_research": cls.ENABLE_STATUTE_RESEARCH,
                "contract_analysis": cls.ENABLE_CONTRACT_ANALYSIS,
                "risk_assessment": cls.ENABLE_RISK_ASSESSMENT,
                "compliance_check": cls.ENABLE_COMPLIANCE_CHECK,
                "legal_drafting": cls.ENABLE_LEGAL_DRAFTING,
                "litigation_prediction": cls.ENABLE_LITIGATION_PREDICTION
            }
        }

    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []

        if not cls.GEMINI_API_KEY:
            issues.append("GEMINI_API_KEY is not set")

        if cls.WEB_PORT == cls.API_PORT:
            issues.append("WEB_PORT and API_PORT must be different")

        if cls.WEB_PORT < 1024 or cls.WEB_PORT > 65535:
            issues.append(f"WEB_PORT {cls.WEB_PORT} is out of valid range (1024-65535)")

        if cls.API_PORT < 1024 or cls.API_PORT > 65535:
            issues.append(f"API_PORT {cls.API_PORT} is out of valid range (1024-65535)")

        if cls.AI_TEMPERATURE < 0 or cls.AI_TEMPERATURE > 1:
            issues.append(f"AI_TEMPERATURE {cls.AI_TEMPERATURE} should be between 0 and 1")

        if cls.TARGET_CASE_SUCCESS_RATE < 0 or cls.TARGET_CASE_SUCCESS_RATE > 1:
            issues.append("TARGET_CASE_SUCCESS_RATE should be between 0 and 1")

        if cls.TARGET_COMPLIANCE_SCORE < 0 or cls.TARGET_COMPLIANCE_SCORE > 1:
            issues.append("TARGET_COMPLIANCE_SCORE should be between 0 and 1")

        # Ensure logs directory exists
        log_dir = Path(cls.LOG_FILE).parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        return issues


# Global config instance
config = Config()
