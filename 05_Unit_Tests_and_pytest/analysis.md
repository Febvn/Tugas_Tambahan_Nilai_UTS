# Analisis: 05 - Unit Tests and pytest

## Deskripsi Tutorial
Tutorial ini memperkenalkan testing dalam Pyramid applications menggunakan pytest. Testing adalah aspek kritis dalam development untuk memastikan kode berfungsi dengan benar dan mencegah regresi saat melakukan perubahan.

## Struktur Kode

### setup.py
```python
from setuptools import setup

requires = [
    'pyramid',
    'pytest',
]

setup(
    name='tutorial',
    install_requires=requires,
)
```
- Menambahkan pytest sebagai dependency untuk testing

### tutorial/__init__.py
```python
from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.scan('.views')
    return config.make_wsgi_app()
```
- Konfigurasi aplikasi dasar dengan routing

### tutorial/views.py
```python
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home', renderer='string')
def home(request):
    return 'Welcome!'

@view_config(route_name='hello', renderer='string')
def hello(request):
    return 'Hello!'
```
- View functions sederhana untuk testing

### tests.py
```python
import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from tutorial.views import home

        request = testing.DummyRequest()
        response = home(request)
        self.assertEqual(response, 'Welcome!')

    def test_hello(self):
        from tutorial.views import hello

        request = testing.DummyRequest()
        response = hello(request)
        self.assertEqual(response, 'Hello!')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Welcome!', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'Hello!', res.body)
```
- Unit tests untuk view functions
- Functional tests untuk testing end-to-end

### pytest.ini
```ini
[tool:pytest]
testpaths = .
python_files = tests.py
python_classes = *Tests
python_functions = test_*
```
- Konfigurasi pytest untuk menemukan dan menjalankan tests

## Jenis Testing

### Unit Tests
- **Tujuan**: Test individual functions/methods secara terpisah
- **Tools**: unittest, pytest
- **Keuntungan**: Cepat, isolated, mudah debug
- **Contoh**: Testing view functions dengan DummyRequest

### Functional Tests
- **Tujuan**: Test aplikasi secara end-to-end
- **Tools**: WebTest
- **Keuntungan**: Test real HTTP requests/responses
- **Contoh**: Testing routes dengan TestApp

## Cara Menjalankan Tests
1. Install dependencies: `pip install -e .`
2. Jalankan tests: `pytest` atau `python -m pytest`
3. Jalankan specific test: `pytest tests.py::ViewTests::test_home`

## Analisis Teknis

### Pyramid Testing Infrastructure
- **testing.setUp()**: Setup test environment Pyramid
- **testing.tearDown()**: Cleanup setelah test
- **DummyRequest**: Mock request object untuk unit tests
- **TestApp**: Wrapper untuk functional testing

### Test Structure Best Practices
1. **setUp/tearDown**: Setup dan cleanup untuk setiap test
2. **Naming Convention**: test_* untuk function names
3. **Assertion Methods**: assertEqual, assertIn, dll
4. **Isolation**: Setiap test independent dari yang lain

### Keuntungan Testing
1. **Bug Prevention**: Catch bugs sebelum production
2. **Refactoring Safety**: Pastikan perubahan tidak break existing functionality
3. **Documentation**: Tests sebagai contoh penggunaan kode
4. **CI/CD Integration**: Automated testing dalam deployment pipeline

### Testing Pyramid vs Web Framework Lain
- **DummyRequest**: Pyramid's mock request object
- **Configurator Testing**: Test configuration setup
- **View Testing**: Test view functions dengan context
- **Integration Testing**: Test dengan real WSGI app

### pytest Features
- **Auto-discovery**: Otomatis menemukan test files
- **Fixtures**: Reusable test setup
- **Parametrization**: Run test dengan multiple inputs
- **Plugins**: Extensible dengan plugins
- **Markers**: Categorize dan filter tests

## Workflow Testing

### Development Workflow dengan Testing:
1. Tulis kode
2. Tulis tests
3. Jalankan tests
4. Refactor jika perlu
5. Jalankan tests lagi
6. Commit dengan confidence

### Test-Driven Development (TDD):
1. Tulis test untuk functionality yang diinginkan
2. Jalankan test (akan fail)
3. Implement functionality
4. Jalankan test (pass)
5. Refactor dan optimize

### Continuous Integration:
- Tests dijalankan otomatis pada setiap commit
- Prevent broken code masuk ke main branch
- Automated deployment hanya jika tests pass

## Kesimpulan
Testing adalah fundamental practice dalam software development. Dengan pytest dan Pyramid's testing utilities, kita dapat membuat aplikasi yang lebih reliable dan maintainable. Unit tests memastikan individual components bekerja dengan benar, sementara functional tests memastikan end-to-end functionality. Kombinasi keduanya memberikan confidence tinggi dalam code quality dan memudahkan refactoring serta maintenance.
