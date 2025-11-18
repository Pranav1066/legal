"""
Utilities package for Legal Intelligence System
"""
from utils.database import db, LegalDatabase
from utils.logger import setup_logger
from utils.validators import validators, Validators, ValidationError

__all__ = [
    'db',
    'LegalDatabase',
    'setup_logger',
    'validators',
    'Validators',
    'ValidationError'
]
