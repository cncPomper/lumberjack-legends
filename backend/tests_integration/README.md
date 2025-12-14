# Integration Tests

This directory contains integration tests for the Lumberjack Legends API using SQLite as the test database.

## Overview

The integration tests verify end-to-end functionality of the API, including:
- Authentication (signup, login, profile management)
- Game sessions (create, end, stats)
- Leaderboard (retrieval, score submission, rankings)
- Complete user workflows

## Test Structure

```
tests_integration/
├── conftest.py                      # Test configuration and fixtures
├── test_auth_integration.py         # Authentication endpoint tests
├── test_game_integration.py         # Game session endpoint tests
├── test_leaderboard_integration.py  # Leaderboard endpoint tests
└── test_end_to_end.py              # Complete user journey tests
```

## Running Tests

### Run all integration tests
```bash
uv run pytest tests_integration/
```

### Run specific test file
```bash
uv run pytest tests_integration/test_auth_integration.py
```

### Run with verbose output
```bash
uv run pytest tests_integration/ -v
```

### Run with coverage
```bash
uv run pytest tests_integration/ --cov=app --cov-report=html
```

### Run specific test class or function
```bash
uv run pytest tests_integration/test_auth_integration.py::TestSignup
uv run pytest tests_integration/test_auth_integration.py::TestSignup::test_successful_signup
```

## Test Database

- Tests use a file-based SQLite database (`test_integration.db`)
- Database is created at the start of the test session
- All data is cleared between tests to ensure isolation
- Database is dropped after all tests complete

## Key Features

### Fixtures

- `client`: TestClient for making API requests
- `db_session`: Direct database access for verification
- `test_user`: Pre-created user for testing authenticated endpoints
- `multiple_users`: Multiple users for leaderboard testing
- `authenticated_client`: Client with authentication token pre-configured

### Test Coverage

1. **Authentication Tests** (`test_auth_integration.py`)
   - User registration and validation
   - Login with password verification
   - Token-based authentication
   - Profile updates

2. **Game Session Tests** (`test_game_integration.py`)
   - Creating game sessions
   - Ending sessions with score/chops/duration
   - Stats calculation
   - High score tracking

3. **Leaderboard Tests** (`test_leaderboard_integration.py`)
   - Leaderboard retrieval with various limits
   - Score submission and ranking
   - User statistics accumulation
   - Integration with game sessions

4. **End-to-End Tests** (`test_end_to_end.py`)
   - Complete user journeys from signup to gameplay
   - Multi-user competition scenarios
   - Data persistence across sessions
   - Edge cases and error handling

## Best Practices

- Each test is independent and doesn't rely on other tests
- Database is reset between tests for isolation
- Tests verify both API responses and database state
- Use descriptive test names that explain what is being tested
- Test both success and failure scenarios

## Differences from Unit Tests

The integration tests in this directory differ from the unit tests in `tests/`:

- **Database**: Uses file-based SQLite vs in-memory SQLite
- **Scope**: Tests complete API flows vs individual components
- **Isolation**: Session-scoped database setup vs function-scoped
- **Focus**: End-to-end functionality vs unit logic

## Adding New Tests

When adding new integration tests:

1. Follow the existing test structure and naming conventions
2. Use appropriate fixtures from `conftest.py`
3. Test both API responses and database state
4. Include tests for error cases
5. Add docstrings explaining what is being tested
6. Ensure tests are independent and can run in any order
