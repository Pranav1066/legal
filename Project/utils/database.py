"""
Database management for Legal Intelligence System
Handles all legal data storage and retrieval operations
"""
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from config import config

logger = logging.getLogger(__name__)


class LegalDatabase:
    """Database manager for Legal Intelligence System"""

    def __init__(self, db_path: str = None):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or config.DATABASE_PATH
        self._ensure_database_exists()
        self._initialize_schema()
        logger.info(f"Database initialized at {self.db_path}")

    def _ensure_database_exists(self):
        """Ensure database file and directory exist"""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()

    def _initialize_schema(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Lawyers/Legal Professionals Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lawyers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    bar_number TEXT UNIQUE,
                    firm TEXT,
                    practice_areas TEXT,
                    jurisdiction TEXT,
                    years_experience INTEGER,
                    specializations TEXT,
                    email TEXT,
                    phone TEXT,
                    win_rate REAL DEFAULT 0.0,
                    total_cases INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Cases Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_number TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    case_type TEXT,
                    practice_area TEXT,
                    jurisdiction TEXT,
                    court TEXT,
                    filing_date DATE,
                    status TEXT,
                    lawyer_id INTEGER,
                    client_name TEXT,
                    opposing_party TEXT,
                    case_summary TEXT,
                    outcome TEXT,
                    outcome_date DATE,
                    settlement_amount REAL,
                    precedent_value TEXT,
                    key_issues TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)

            # Legal Documents Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    case_id INTEGER,
                    lawyer_id INTEGER,
                    document_content TEXT,
                    file_path TEXT,
                    jurisdiction TEXT,
                    practice_area TEXT,
                    creation_date DATE,
                    last_modified DATE,
                    status TEXT DEFAULT 'draft',
                    risk_score REAL,
                    compliance_status TEXT,
                    review_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)

            # Statutes & Regulations Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statutes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    statute_code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    jurisdiction TEXT,
                    category TEXT,
                    full_text TEXT,
                    summary TEXT,
                    effective_date DATE,
                    last_amended DATE,
                    status TEXT DEFAULT 'active',
                    citation_count INTEGER DEFAULT 0,
                    related_statutes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Case Law / Precedents Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS precedents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_name TEXT NOT NULL,
                    citation TEXT UNIQUE,
                    court TEXT,
                    jurisdiction TEXT,
                    decision_date DATE,
                    practice_area TEXT,
                    legal_issue TEXT,
                    holding TEXT,
                    reasoning TEXT,
                    dissent TEXT,
                    importance_score REAL,
                    citation_count INTEGER DEFAULT 0,
                    overruled BOOLEAN DEFAULT FALSE,
                    related_cases TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Contracts Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contract_name TEXT NOT NULL,
                    contract_type TEXT,
                    parties TEXT NOT NULL,
                    execution_date DATE,
                    effective_date DATE,
                    expiration_date DATE,
                    jurisdiction TEXT,
                    governing_law TEXT,
                    contract_value REAL,
                    status TEXT DEFAULT 'active',
                    risk_level TEXT,
                    risk_score REAL,
                    key_terms TEXT,
                    obligations TEXT,
                    penalties TEXT,
                    termination_clauses TEXT,
                    document_id INTEGER,
                    lawyer_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES legal_documents (id),
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)

            # Compliance Requirements Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compliance_requirements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requirement_code TEXT UNIQUE NOT NULL,
                    framework TEXT NOT NULL,
                    category TEXT,
                    description TEXT NOT NULL,
                    jurisdiction TEXT,
                    industry TEXT,
                    mandatory BOOLEAN DEFAULT TRUE,
                    penalty_description TEXT,
                    compliance_deadline DATE,
                    related_statutes TEXT,
                    implementation_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Deadlines & Calendar Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS deadlines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER,
                    lawyer_id INTEGER,
                    deadline_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    due_date DATE NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    reminder_sent BOOLEAN DEFAULT FALSE,
                    completed_date DATE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (case_id) REFERENCES cases (id),
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)

            # Legal Research Sessions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    lawyer_id INTEGER,
                    case_id INTEGER,
                    research_query TEXT,
                    practice_area TEXT,
                    jurisdiction TEXT,
                    findings TEXT,
                    relevant_cases TEXT,
                    relevant_statutes TEXT,
                    recommendations TEXT,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id),
                    FOREIGN KEY (case_id) REFERENCES cases (id)
                )
            """)

            # Analysis Results Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_type TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id INTEGER NOT NULL,
                    lawyer_id INTEGER,
                    result_summary TEXT,
                    detailed_analysis TEXT,
                    confidence_score REAL,
                    risk_factors TEXT,
                    recommendations TEXT,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)

            conn.commit()
            logger.info("Database schema initialized successfully")

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a SELECT query and return results as list of dicts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def execute_insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert data into table and return last row id"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(data.values()))
            return cursor.lastrowid

    def execute_update(self, table: str, data: Dict[str, Any], where: str, params: tuple = ()) -> int:
        """Update table and return number of rows affected"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE {where}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(data.values()) + params)
            return cursor.rowcount

    # Lawyer Operations
    def add_lawyer(self, lawyer_data: Dict[str, Any]) -> int:
        """Add a new lawyer"""
        return self.execute_insert('lawyers', lawyer_data)

    def get_lawyer_by_id(self, lawyer_id: int) -> Optional[Dict]:
        """Get lawyer by ID"""
        results = self.execute_query("SELECT * FROM lawyers WHERE id = ?", (lawyer_id,))
        return results[0] if results else None

    def get_all_lawyers(self) -> List[Dict]:
        """Get all lawyers"""
        return self.execute_query("SELECT * FROM lawyers ORDER BY name")

    # Case Operations
    def add_case(self, case_data: Dict[str, Any]) -> int:
        """Add a new case"""
        return self.execute_insert('cases', case_data)

    def get_case_by_id(self, case_id: int) -> Optional[Dict]:
        """Get case by ID"""
        results = self.execute_query("SELECT * FROM cases WHERE id = ?", (case_id,))
        return results[0] if results else None

    def get_lawyer_cases(self, lawyer_id: int) -> List[Dict]:
        """Get all cases for a lawyer"""
        return self.execute_query("SELECT * FROM cases WHERE lawyer_id = ? ORDER BY filing_date DESC", (lawyer_id,))

    def get_open_cases(self) -> List[Dict]:
        """Get all open cases"""
        return self.execute_query("SELECT * FROM cases WHERE status IN ('active', 'pending') ORDER BY filing_date DESC")

    # Document Operations
    def add_document(self, document_data: Dict[str, Any]) -> int:
        """Add a new legal document"""
        return self.execute_insert('legal_documents', document_data)

    def get_document_by_id(self, document_id: int) -> Optional[Dict]:
        """Get document by ID"""
        results = self.execute_query("SELECT * FROM legal_documents WHERE id = ?", (document_id,))
        return results[0] if results else None

    def get_case_documents(self, case_id: int) -> List[Dict]:
        """Get all documents for a case"""
        return self.execute_query("SELECT * FROM legal_documents WHERE case_id = ? ORDER BY creation_date DESC", (case_id,))

    # Statute Operations
    def add_statute(self, statute_data: Dict[str, Any]) -> int:
        """Add a new statute"""
        return self.execute_insert('statutes', statute_data)

    def search_statutes(self, jurisdiction: str = None, category: str = None, keyword: str = None) -> List[Dict]:
        """Search statutes"""
        query = "SELECT * FROM statutes WHERE 1=1"
        params = []

        if jurisdiction:
            query += " AND jurisdiction = ?"
            params.append(jurisdiction)
        if category:
            query += " AND category = ?"
            params.append(category)
        if keyword:
            query += " AND (title LIKE ? OR summary LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        query += " ORDER BY citation_count DESC"
        return self.execute_query(query, tuple(params))

    # Precedent Operations
    def add_precedent(self, precedent_data: Dict[str, Any]) -> int:
        """Add a new precedent"""
        return self.execute_insert('precedents', precedent_data)

    def search_precedents(self, practice_area: str = None, jurisdiction: str = None, keyword: str = None) -> List[Dict]:
        """Search precedents"""
        query = "SELECT * FROM precedents WHERE overruled = FALSE"
        params = []

        if practice_area:
            query += " AND practice_area = ?"
            params.append(practice_area)
        if jurisdiction:
            query += " AND jurisdiction = ?"
            params.append(jurisdiction)
        if keyword:
            query += " AND (case_name LIKE ? OR legal_issue LIKE ? OR keywords LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])

        query += " ORDER BY importance_score DESC, citation_count DESC"
        return self.execute_query(query, tuple(params))

    # Contract Operations
    def add_contract(self, contract_data: Dict[str, Any]) -> int:
        """Add a new contract"""
        return self.execute_insert('contracts', contract_data)

    def get_active_contracts(self) -> List[Dict]:
        """Get all active contracts"""
        return self.execute_query("SELECT * FROM contracts WHERE status = 'active' ORDER BY effective_date DESC")

    # Compliance Operations
    def add_compliance_requirement(self, requirement_data: Dict[str, Any]) -> int:
        """Add a new compliance requirement"""
        return self.execute_insert('compliance_requirements', requirement_data)

    def get_compliance_requirements(self, framework: str = None, jurisdiction: str = None) -> List[Dict]:
        """Get compliance requirements"""
        query = "SELECT * FROM compliance_requirements WHERE 1=1"
        params = []

        if framework:
            query += " AND framework = ?"
            params.append(framework)
        if jurisdiction:
            query += " AND jurisdiction = ?"
            params.append(jurisdiction)

        return self.execute_query(query, tuple(params))

    # Deadline Operations
    def add_deadline(self, deadline_data: Dict[str, Any]) -> int:
        """Add a new deadline"""
        return self.execute_insert('deadlines', deadline_data)

    def get_upcoming_deadlines(self, days: int = 30) -> List[Dict]:
        """Get upcoming deadlines"""
        query = """
            SELECT * FROM deadlines
            WHERE status = 'pending'
            AND date(due_date) BETWEEN date('now') AND date('now', '+' || ? || ' days')
            ORDER BY due_date ASC
        """
        return self.execute_query(query, (days,))

    # Research Session Operations
    def add_research_session(self, session_data: Dict[str, Any]) -> int:
        """Add a new research session"""
        return self.execute_insert('research_sessions', session_data)

    def get_lawyer_research_sessions(self, lawyer_id: int) -> List[Dict]:
        """Get research sessions for a lawyer"""
        return self.execute_query("SELECT * FROM research_sessions WHERE lawyer_id = ? ORDER BY session_date DESC", (lawyer_id,))

    # Analysis Operations
    def save_analysis_result(self, analysis_data: Dict[str, Any]) -> int:
        """Save analysis result"""
        return self.execute_insert('analysis_results', analysis_data)

    def get_entity_analyses(self, entity_type: str, entity_id: int) -> List[Dict]:
        """Get all analyses for an entity"""
        return self.execute_query(
            "SELECT * FROM analysis_results WHERE entity_type = ? AND entity_id = ? ORDER BY analysis_date DESC",
            (entity_type, entity_id)
        )

    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        stats = {}
        tables = ['lawyers', 'cases', 'legal_documents', 'statutes', 'precedents',
                  'contracts', 'compliance_requirements', 'deadlines', 'research_sessions']

        for table in tables:
            result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            stats[f"{table}_count"] = result[0]['count'] if result else 0

        return stats


# Global database instance
db = LegalDatabase()
