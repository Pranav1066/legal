#!/bin/bash

# Run tests for Financial Intelligence System
cd "$(dirname "$0")"
python -m pytest tests.py -v --tb=short
