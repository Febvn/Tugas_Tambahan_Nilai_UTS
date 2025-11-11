# Tutorial 06: Functional Testing with WebTest

## Overview
This tutorial demonstrates functional testing in Pyramid applications using WebTest. Functional testing focuses on testing the application from the user's perspective, simulating HTTP requests and verifying responses.

## Key Concepts

### Functional Testing vs Unit Testing
- **Unit Testing**: Tests individual components in isolation
- **Functional Testing**: Tests the entire application stack end-to-end

### WebTest Framework
WebTest is a Python library that provides a simple interface for testing WSGI applications. It allows you to make HTTP requests to your application and inspect the responses.

## Implementation Details

### Application Structure
The application consists of:
- `setup.py`: Defines dependencies including `webtest`
- `tutorial/__init__.py`: Main application configuration with routes
- `tutorial/views.py`: Simple view functions returning string responses
- `tests.py`: Both unit and functional tests

### Test Classes

#### ViewTests (Unit Tests)
```python
class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .tutorial.views import home
        request = testing.DummyRequest()
        response = home(request)
        self.assertEqual(response, 'Welcome!')
```

This class tests individual view functions using Pyramid's testing utilities.

#### FunctionalTests (Functional Tests)
```python
class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Welcome!', res.body)
```

This class tests the full application stack using WebTest's TestApp.

## WebTest Features

### TestApp Methods
- `get(url, status=None)`: Makes a GET request
- `post(url, data, status=None)`: Makes a POST request
- `put()`, `delete()`, etc.: Other HTTP methods

### Response Object
- `res.status`: HTTP status code
- `res.body`: Response body as bytes
- `res.json`: Parsed JSON response
- `res.headers`: Response headers

## Running Tests

### Installation
```bash
pip install -e .
```

### Execute Tests
```bash
python -m pytest tests.py -v
```

### Expected Output
```
tests.py::ViewTests::test_home PASSED
tests.py::ViewTests::test_hello PASSED
tests.py::FunctionalTests::test_home PASSED
tests.py::FunctionalTests::test_hello PASSED
```

## Analysis

### Advantages of Functional Testing
1. **End-to-End Validation**: Tests the complete request-response cycle
2. **Integration Testing**: Verifies all components work together
3. **User Perspective**: Simulates real user interactions
4. **Regression Prevention**: Catches issues that unit tests might miss

### WebTest Benefits
1. **Simple API**: Easy to write and understand tests
2. **WSGI Compatible**: Works with any WSGI application
3. **Comprehensive**: Supports all HTTP methods and features
4. **Fast**: Lightweight and quick to execute

### Best Practices
1. **Test Status Codes**: Always verify expected HTTP status codes
2. **Check Content**: Validate response content and structure
3. **Test Edge Cases**: Include error conditions and edge cases
4. **Organize Tests**: Group related tests in classes
5. **Use Fixtures**: Set up test data appropriately

### Comparison with Unit Tests
- **Unit Tests**: Fast, isolated, test individual functions
- **Functional Tests**: Slower, integrated, test complete workflows

### When to Use Functional Tests
- Testing complete user workflows
- Verifying integration between components
- Testing API endpoints
- Validating error handling
- Regression testing

## Conclusion
Functional testing with WebTest provides a powerful way to ensure your Pyramid application works correctly from the user's perspective. It complements unit testing by validating the entire application stack and catching integration issues that unit tests might miss.
