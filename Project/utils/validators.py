"""
Input validation utilities for Legal Intelligence System
"""
import re
from datetime import datetime
from typing import Any, Dict, List, Optional


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class Validators:
    """Collection of validation methods for legal data"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it's 10 digits
        return bool(re.match(r'^\d{10}$', cleaned))

    @staticmethod
    def validate_bar_number(bar_number: str) -> bool:
        """Validate bar number format (alphanumeric, 6-15 chars)"""
        return bool(re.match(r'^[A-Z0-9]{6,15}$', bar_number.upper()))

    @staticmethod
    def validate_case_number(case_number: str) -> bool:
        """Validate case number format"""
        # Common format: XX-YYYY-NNNNNN (e.g., CV-2024-001234)
        return bool(re.match(r'^[A-Z]{2,4}-\d{4}-\d{4,8}$', case_number))

    @staticmethod
    def validate_date(date_str: str, date_format: str = '%Y-%m-%d') -> bool:
        """Validate date string format"""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_jurisdiction(jurisdiction: str, valid_jurisdictions: List[str]) -> bool:
        """Validate jurisdiction against list of valid jurisdictions"""
        return jurisdiction in valid_jurisdictions

    @staticmethod
    def validate_practice_area(practice_area: str, valid_areas: List[str]) -> bool:
        """Validate practice area against list of valid areas"""
        return practice_area in valid_areas

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Validate that all required fields are present and non-empty

        Args:
            data: Dictionary to validate
            required_fields: List of required field names

        Returns:
            List of missing or empty fields
        """
        missing = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing.append(field)
        return missing

    @staticmethod
    def validate_lawyer_data(lawyer_data: Dict[str, Any]) -> List[str]:
        """
        Validate lawyer data

        Returns:
            List of validation errors
        """
        errors = []

        # Required fields
        required = ['name', 'bar_number', 'practice_areas', 'jurisdiction']
        missing = Validators.validate_required_fields(lawyer_data, required)
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

        # Bar number format
        if 'bar_number' in lawyer_data:
            if not Validators.validate_bar_number(lawyer_data['bar_number']):
                errors.append("Invalid bar number format (should be 6-15 alphanumeric characters)")

        # Email format
        if 'email' in lawyer_data and lawyer_data['email']:
            if not Validators.validate_email(lawyer_data['email']):
                errors.append("Invalid email format")

        # Phone format
        if 'phone' in lawyer_data and lawyer_data['phone']:
            if not Validators.validate_phone(lawyer_data['phone']):
                errors.append("Invalid phone number format")

        # Years of experience
        if 'years_experience' in lawyer_data:
            try:
                years = int(lawyer_data['years_experience'])
                if years < 0 or years > 70:
                    errors.append("Years of experience must be between 0 and 70")
            except (ValueError, TypeError):
                errors.append("Years of experience must be a valid number")

        return errors

    @staticmethod
    def validate_case_data(case_data: Dict[str, Any]) -> List[str]:
        """
        Validate case data

        Returns:
            List of validation errors
        """
        errors = []

        # Required fields
        required = ['case_number', 'title', 'case_type', 'jurisdiction']
        missing = Validators.validate_required_fields(case_data, required)
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

        # Case number format
        if 'case_number' in case_data:
            if not Validators.validate_case_number(case_data['case_number']):
                errors.append("Invalid case number format (should be XX-YYYY-NNNNNN)")

        # Filing date
        if 'filing_date' in case_data and case_data['filing_date']:
            if not Validators.validate_date(case_data['filing_date']):
                errors.append("Invalid filing date format (should be YYYY-MM-DD)")

        # Outcome date
        if 'outcome_date' in case_data and case_data['outcome_date']:
            if not Validators.validate_date(case_data['outcome_date']):
                errors.append("Invalid outcome date format (should be YYYY-MM-DD)")

        # Settlement amount
        if 'settlement_amount' in case_data and case_data['settlement_amount']:
            try:
                amount = float(case_data['settlement_amount'])
                if amount < 0:
                    errors.append("Settlement amount cannot be negative")
            except (ValueError, TypeError):
                errors.append("Settlement amount must be a valid number")

        return errors

    @staticmethod
    def validate_contract_data(contract_data: Dict[str, Any]) -> List[str]:
        """
        Validate contract data

        Returns:
            List of validation errors
        """
        errors = []

        # Required fields
        required = ['contract_name', 'contract_type', 'parties']
        missing = Validators.validate_required_fields(contract_data, required)
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

        # Date validations
        date_fields = ['execution_date', 'effective_date', 'expiration_date']
        for field in date_fields:
            if field in contract_data and contract_data[field]:
                if not Validators.validate_date(contract_data[field]):
                    errors.append(f"Invalid {field} format (should be YYYY-MM-DD)")

        # Contract value
        if 'contract_value' in contract_data and contract_data['contract_value']:
            try:
                value = float(contract_data['contract_value'])
                if value < 0:
                    errors.append("Contract value cannot be negative")
            except (ValueError, TypeError):
                errors.append("Contract value must be a valid number")

        # Risk score
        if 'risk_score' in contract_data and contract_data['risk_score']:
            try:
                score = float(contract_data['risk_score'])
                if score < 0 or score > 1:
                    errors.append("Risk score must be between 0 and 1")
            except (ValueError, TypeError):
                errors.append("Risk score must be a valid number")

        return errors

    @staticmethod
    def validate_deadline_data(deadline_data: Dict[str, Any]) -> List[str]:
        """
        Validate deadline data

        Returns:
            List of validation errors
        """
        errors = []

        # Required fields
        required = ['deadline_type', 'description', 'due_date']
        missing = Validators.validate_required_fields(deadline_data, required)
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

        # Due date
        if 'due_date' in deadline_data and deadline_data['due_date']:
            if not Validators.validate_date(deadline_data['due_date']):
                errors.append("Invalid due date format (should be YYYY-MM-DD)")

        # Priority
        if 'priority' in deadline_data:
            valid_priorities = ['low', 'medium', 'high', 'critical']
            if deadline_data['priority'] not in valid_priorities:
                errors.append(f"Priority must be one of: {', '.join(valid_priorities)}")

        return errors

    @staticmethod
    def sanitize_text(text: str, max_length: int = None) -> str:
        """
        Sanitize text input by removing potentially harmful characters

        Args:
            text: Input text
            max_length: Maximum length to truncate to

        Returns:
            Sanitized text
        """
        if not text:
            return ""

        # Remove control characters except newlines and tabs
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

        # Truncate if needed
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized.strip()

    @staticmethod
    def validate_score(score: float, min_val: float = 0.0, max_val: float = 1.0) -> bool:
        """
        Validate that a score is within acceptable range

        Args:
            score: Score to validate
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value

        Returns:
            True if valid, False otherwise
        """
        try:
            score_float = float(score)
            return min_val <= score_float <= max_val
        except (ValueError, TypeError):
            return False


# Global validators instance
validators = Validators()
