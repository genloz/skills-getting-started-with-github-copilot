# FastAPI Tests

This directory contains comprehensive tests for the Mergington High School Activities API built with FastAPI.

## Test Structure

- **`conftest.py`** - Test configuration and fixtures
- **`test_activities.py`** - Core API endpoint tests for activities
- **`test_app.py`** - Static file serving and general app functionality tests
- **`test_edge_cases.py`** - Edge cases and integration tests

## Test Coverage

The test suite provides **100% code coverage** for the FastAPI application, testing:

### Core Functionality
- ✅ Get all activities
- ✅ Sign up for activities
- ✅ Unregister from activities
- ✅ Root endpoint redirect

### Error Handling
- ✅ Nonexistent activities
- ✅ Duplicate signups
- ✅ Unregistering non-participants
- ✅ Invalid HTTP methods

### Static Files
- ✅ HTML, CSS, and JavaScript file serving
- ✅ 404 handling for missing files

### Edge Cases
- ✅ URL encoding in activity names
- ✅ Email validation and special characters
- ✅ Case sensitivity
- ✅ Missing parameters
- ✅ Data persistence across requests

## Running Tests

### Quick Run
```bash
pytest tests/
```

### With Coverage
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Using the Test Runner Script
```bash
./run_tests.sh
```

### With HTML Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
```
This generates an interactive HTML coverage report in `htmlcov/index.html`.

## Test Configuration

- **pytest.ini** - Pytest configuration with test discovery settings
- **requirements.txt** - Updated with testing dependencies:
  - `pytest` - Testing framework
  - `httpx` - HTTP client for FastAPI testing
  - `pytest-cov` - Coverage reporting

## Fixtures

### `client`
Provides a FastAPI TestClient for making HTTP requests to the API.

### `reset_activities`
Resets the activities data to its original state before each test, ensuring test isolation.

## Test Philosophy

- **Isolation**: Each test is independent and doesn't affect others
- **Comprehensive**: Tests cover happy paths, error cases, and edge cases
- **Realistic**: Tests use realistic data and scenarios
- **Fast**: Tests run quickly for rapid feedback during development

## Continuous Integration

These tests are designed to be easily integrated into CI/CD pipelines:
- No external dependencies (uses in-memory data)
- Fast execution (< 1 second)
- Clear pass/fail results
- Detailed coverage reporting