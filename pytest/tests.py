"""
Legal Intelligence System - Comprehensive Test Suite
Single file with 10+ essential test cases
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from utils.database import LegalDatabase
from utils.validators import Validators


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def test_db():
    """Create a fresh test database"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    db = LegalDatabase(db_path)
    yield db

    # Cleanup
    try:
        if hasattr(db, 'conn'):
            db.conn.close()
        os.unlink(db_path)
    except:
        pass


@pytest.fixture
def sample_lawyer():
    """Sample lawyer data"""
    return {
        'name': 'John Doe',
        'email': 'john.doe@lawfirm.com',
        'phone': '5551234567',
        'practice_areas': 'Corporate Law',
        'bar_number': 'BAR123456',
        'jurisdiction': 'Federal',
        'years_experience': 10,
        'firm': 'Doe & Associates'
    }


@pytest.fixture
def sample_case():
    """Sample case data"""
    return {
        'case_number': 'CV-2024-001234',
        'title': 'Test Corp v. Sample Inc',
        'case_type': 'Civil',
        'status': 'Active',
        'filing_date': '2024-01-15',
        'jurisdiction': 'Federal',
        'court': 'Federal District Court'
    }


# ============================================================================
# TEST CASES (10+)
# ============================================================================

def test_01_config_loads_successfully():
    """Test Case 1: Configuration loads without errors"""
    # Act
    config = Config()

    # Assert
    assert config is not None
    assert hasattr(config, 'GEMINI_API_KEY')
    assert hasattr(config, 'AI_MODEL')
    assert hasattr(config, 'DATABASE_PATH')
    print("✓ Test 1: Configuration loaded successfully")


def test_02_config_has_correct_defaults():
    """Test Case 2: Configuration has correct default values"""
    # Act
    config = Config()

    # Assert
    assert config.AI_MODEL == "gemini-2.5-flash-lite"
    assert config.AI_TEMPERATURE == 0.7
    assert config.WEB_PORT == 8501
    assert config.API_PORT == 8004
    assert config.ENABLE_CONTRACT_ANALYSIS is True
    print("✓ Test 2: Default configuration values are correct")


def test_03_email_validation_works():
    """Test Case 3: Email validation works correctly"""
    # Valid emails
    assert Validators.validate_email("john.doe@lawfirm.com") is True
    assert Validators.validate_email("attorney@example.org") is True

    # Invalid emails
    assert Validators.validate_email("not-an-email") is False
    assert Validators.validate_email("@example.com") is False
    assert Validators.validate_email("") is False
    print("✓ Test 3: Email validation working correctly")


def test_04_phone_validation_works():
    """Test Case 4: Phone validation works correctly"""
    # Valid phones
    assert Validators.validate_phone("5551234567") is True
    assert Validators.validate_phone("(555) 123-4567") is True
    assert Validators.validate_phone("555-123-4567") is True

    # Invalid phones
    assert Validators.validate_phone("123") is False
    assert Validators.validate_phone("") is False
    print("✓ Test 4: Phone validation working correctly")


def test_05_date_validation_works():
    """Test Case 5: Date validation works correctly"""
    # Valid dates
    assert Validators.validate_date("2024-01-15") is True
    assert Validators.validate_date("2023-12-31") is True

    # Invalid dates
    assert Validators.validate_date("01/15/2024") is False  # Wrong format
    assert Validators.validate_date("2024-13-01") is False  # Invalid month
    assert Validators.validate_date("not-a-date") is False
    print("✓ Test 5: Date validation working correctly")


def test_06_database_initializes_successfully(test_db):
    """Test Case 6: Database initializes with correct schema"""
    # Assert
    assert test_db is not None

    # Check database stats work (which means database is initialized)
    stats = test_db.get_database_stats()
    assert stats is not None
    assert 'lawyers_count' in stats
    assert 'cases_count' in stats
    print("✓ Test 6: Database initialized with correct schema")


def test_07_add_lawyer_to_database(test_db, sample_lawyer):
    """Test Case 7: Add lawyer to database successfully"""
    # Act
    lawyer_id = test_db.add_lawyer(sample_lawyer)

    # Assert
    assert lawyer_id is not None
    assert lawyer_id > 0

    # Verify lawyer was added
    lawyer = test_db.get_lawyer_by_id(lawyer_id)
    assert lawyer is not None
    assert lawyer['name'] == sample_lawyer['name']
    assert lawyer['email'] == sample_lawyer['email']
    assert lawyer['bar_number'] == sample_lawyer['bar_number']
    print(f"✓ Test 7: Lawyer added successfully (ID: {lawyer_id})")


def test_08_get_nonexistent_lawyer_returns_none(test_db):
    """Test Case 8: Getting non-existent lawyer returns None"""
    # Act
    lawyer = test_db.get_lawyer_by_id(99999)

    # Assert
    assert lawyer is None
    print("✓ Test 8: Non-existent lawyer returns None correctly")


def test_09_add_case_to_database(test_db, sample_lawyer, sample_case):
    """Test Case 9: Add case to database successfully"""
    # Arrange - First add a lawyer
    lawyer_id = test_db.add_lawyer(sample_lawyer)
    sample_case['lawyer_id'] = lawyer_id

    # Act
    case_id = test_db.add_case(sample_case)

    # Assert
    assert case_id is not None
    assert case_id > 0

    # Verify case was added
    case = test_db.get_case_by_id(case_id)
    assert case is not None
    assert case['title'] == sample_case['title']
    assert case['case_number'] == sample_case['case_number']
    assert case['lawyer_id'] == lawyer_id
    print(f"✓ Test 9: Case added successfully (ID: {case_id})")


def test_10_get_cases_for_lawyer(test_db, sample_lawyer, sample_case):
    """Test Case 10: Get all cases for a specific lawyer"""
    # Arrange
    lawyer_id = test_db.add_lawyer(sample_lawyer)
    sample_case['lawyer_id'] = lawyer_id

    # Add multiple cases
    case_id_1 = test_db.add_case(sample_case)

    case_2 = sample_case.copy()
    case_2['case_number'] = 'CV-2024-002345'
    case_2['title'] = 'Another Test Case'
    case_id_2 = test_db.add_case(case_2)

    # Act
    cases = test_db.get_lawyer_cases(lawyer_id)

    # Assert
    assert len(cases) == 2
    assert cases[0]['lawyer_id'] == lawyer_id
    assert cases[1]['lawyer_id'] == lawyer_id
    print(f"✓ Test 10: Retrieved {len(cases)} cases for lawyer {lawyer_id}")


def test_11_database_statistics_work(test_db, sample_lawyer, sample_case):
    """Test Case 11: Database statistics return correct counts"""
    # Arrange - Add sample data
    lawyer_id = test_db.add_lawyer(sample_lawyer)
    sample_case['lawyer_id'] = lawyer_id
    test_db.add_case(sample_case)

    # Act
    stats = test_db.get_database_stats()

    # Assert
    assert stats is not None
    assert stats['lawyers_count'] >= 1
    assert stats['cases_count'] >= 1
    assert 'legal_documents_count' in stats
    print(f"✓ Test 11: Database stats - {stats['lawyers_count']} lawyers, {stats['cases_count']} cases")


def test_12_lawyer_data_validation(sample_lawyer):
    """Test Case 12: Lawyer data validation works correctly"""
    # Valid lawyer data
    errors = Validators.validate_lawyer_data(sample_lawyer)
    assert len(errors) == 0

    # Invalid lawyer data (missing required fields)
    invalid_lawyer = {'email': 'test@example.com'}
    errors = Validators.validate_lawyer_data(invalid_lawyer)
    assert len(errors) > 0
    print("✓ Test 12: Lawyer data validation working correctly")


def test_13_case_data_validation(sample_case):
    """Test Case 13: Case data validation works correctly"""
    # Valid case data
    errors = Validators.validate_case_data(sample_case)
    assert len(errors) == 0

    # Invalid case data (wrong date format)
    invalid_case = sample_case.copy()
    invalid_case['filing_date'] = '01/15/2024'  # Wrong format
    errors = Validators.validate_case_data(invalid_case)
    assert len(errors) > 0
    print("✓ Test 13: Case data validation working correctly")


def test_14_practice_areas_list_loaded():
    """Test Case 14: Practice areas list loads from config"""
    # Act
    config = Config()

    # Assert
    assert isinstance(config.DEFAULT_PRACTICE_AREAS, list)
    assert len(config.DEFAULT_PRACTICE_AREAS) > 0
    assert "Corporate Law" in config.DEFAULT_PRACTICE_AREAS
    assert "Criminal Law" in config.DEFAULT_PRACTICE_AREAS
    print(f"✓ Test 14: Loaded {len(config.DEFAULT_PRACTICE_AREAS)} practice areas")


def test_15_compliance_frameworks_list_loaded():
    """Test Case 15: Compliance frameworks list loads from config"""
    # Act
    config = Config()

    # Assert
    assert isinstance(config.COMPLIANCE_FRAMEWORKS, list)
    assert len(config.COMPLIANCE_FRAMEWORKS) > 0
    assert "GDPR" in config.COMPLIANCE_FRAMEWORKS
    assert "HIPAA" in config.COMPLIANCE_FRAMEWORKS
    assert "SOX" in config.COMPLIANCE_FRAMEWORKS
    print(f"✓ Test 15: Loaded {len(config.COMPLIANCE_FRAMEWORKS)} compliance frameworks")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  Legal Intelligence System - Test Suite")
    print("="*70 + "\n")

    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
