#!/bin/bash

# FastAPI Test Runner Script
# This script runs all tests for the Mergington High School Activities API

echo "🧪 Running FastAPI Tests for Mergington High School Activities API"
echo "=================================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Using virtual environment..."
    PYTHON_CMD="./.venv/bin/python"
else
    echo "📦 Using system Python..."
    PYTHON_CMD="python3"
fi

echo ""
echo "🔍 Running tests with coverage..."
$PYTHON_CMD -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "📊 Coverage report generated in htmlcov/index.html"
echo "🎉 Tests completed!"