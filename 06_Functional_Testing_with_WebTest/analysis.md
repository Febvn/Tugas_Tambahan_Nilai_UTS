# Tutorial 06: Functional Testing dengan WebTest

## Gambaran Umum
Tutorial ini mendemonstrasikan functional testing dalam aplikasi Pyramid menggunakan WebTest. Functional testing berfokus pada pengujian aplikasi dari perspektif pengguna, mensimulasikan HTTP requests dan memverifikasi responses.

## Konsep Kunci

### Functional Testing vs Unit Testing
- **Unit Testing**: Menguji komponen individual secara terpisah
- **Functional Testing**: Menguji seluruh stack aplikasi end-to-end

### Framework WebTest
WebTest adalah library Python yang menyediakan interface sederhana untuk testing aplikasi WSGI. Library ini memungkinkan Anda membuat HTTP requests ke aplikasi dan memeriksa responses.

## Detail Implementasi

### Struktur Aplikasi
Aplikasi terdiri dari:
- `setup.py`: Mendefinisikan dependensi termasuk `webtest`
- `tutorial/__init__.py`: Konfigurasi aplikasi utama dengan routes
- `tutorial/views.py`: Fungsi view sederhana yang mengembalikan string responses
- `tests.py`: Unit tests dan functional tests

### Kelas Test

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

Kelas ini menguji fungsi view individual menggunakan utilities testing Pyramid.

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

Kelas ini menguji full application stack menggunakan TestApp dari WebTest.

## Fitur WebTest

### Method TestApp
- `get(url, status=None)`: Membuat GET request
- `post(url, data, status=None)`: Membuat POST request
- `put()`, `delete()`, dll.: HTTP methods lainnya

### Objek Response
- `res.status`: Kode status HTTP
- `res.body`: Body response sebagai bytes
- `res.json`: Response JSON yang di-parse
- `res.headers`: Headers response

## Menjalankan Tests

### Instalasi
```bash
pip install -e .
```

### Eksekusi Tests
```bash
python -m pytest tests.py -v
```

### Output yang Diharapkan
```
tests.py::ViewTests::test_home PASSED
tests.py::ViewTests::test_hello PASSED
tests.py::FunctionalTests::test_home PASSED
tests.py::FunctionalTests::test_hello PASSED
```

## Analisis

### Keuntungan Functional Testing
1. **Validasi End-to-End**: Menguji siklus request-response lengkap
2. **Integration Testing**: Memverifikasi semua komponen bekerja bersama
3. **Perspektif Pengguna**: Mensimulasikan interaksi pengguna nyata
4. **Pencegahan Regresi**: Menangkap masalah yang mungkin terlewat oleh unit tests

### Manfaat WebTest
1. **API Sederhana**: Mudah menulis dan memahami tests
2. **Kompatibel WSGI**: Bekerja dengan aplikasi WSGI apapun
3. **Komprehensif**: Mendukung semua HTTP methods dan fitur
4. **Cepat**: Ringan dan cepat dieksekusi

### Best Practices
1. **Test Status Codes**: Selalu verifikasi kode status HTTP yang diharapkan
2. **Periksa Konten**: Validasi konten dan struktur response
3. **Test Edge Cases**: Sertakan kondisi error dan edge cases
4. **Organisasi Tests**: Kelompokkan tests terkait dalam kelas
5. **Gunakan Fixtures**: Setup data test dengan tepat

### Perbandingan dengan Unit Tests
- **Unit Tests**: Cepat, terisolasi, menguji fungsi individual
- **Functional Tests**: Lebih lambat, terintegrasi, menguji workflow lengkap

### Kapan Menggunakan Functional Tests
- Testing workflow pengguna lengkap
- Memverifikasi integrasi antar komponen
- Testing API endpoints
- Validasi error handling
- Regression testing

## Kesimpulan
Functional testing dengan WebTest menyediakan cara yang powerful untuk memastikan aplikasi Pyramid Anda bekerja dengan benar dari perspektif pengguna. Ini melengkapi unit testing dengan memvalidasi seluruh application stack dan menangkap masalah integrasi yang mungkin terlewat oleh unit tests.