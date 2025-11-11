# Analisis: 02 - Python Packages for Pyramid Applications

## Deskripsi Tutorial
Tutorial ini menunjukkan bagaimana membuat aplikasi Pyramid sebagai paket Python yang dapat didistribusikan, menggunakan setup.py dan struktur paket standar.

## Struktur Kode

### setup.py
```python
from setuptools import setup

requires = [
    'pyramid',
]

setup(
    name='tutorial',
    install_requires=requires,
)
```
- Menggunakan setuptools untuk mendefinisikan paket
- Menentukan dependensi (pyramid) dalam `install_requires`
- Nama paket adalah 'tutorial'

### tutorial/__init__.py
```python
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.scan('.views')
    return config.make_wsgi_app()
```
- Fungsi `main` sebagai entry point aplikasi
- Menggunakan Configurator untuk setup routing
- `config.scan('.views')` untuk auto-discovery view functions

### tutorial/views.py
```python
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home', renderer='json')
def home(request):
    return {'name': 'Home View'}
```
- View function dengan decorator `@view_config`
- Menggunakan JSON renderer
- Return dictionary yang akan di-serialize ke JSON

### development.ini
```ini
[app:main]
use = egg:tutorial

[server:main]
use = egg:pyramid#wsgiref
host = 0.0.0.0
port = 6543
```
- Konfigurasi aplikasi menggunakan entry point 'egg:tutorial'
- Server menggunakan WSGI ref dari Pyramid
- Port default 6543

## Cara Menjalankan
1. Install paket: `pip install -e .`
2. Jalankan server: `pserve development.ini`
3. Akses: http://localhost:6543

## Analisis Teknis

### Keuntungan Pendekatan Paket Python:
1. **Distribusi**: Mudah didistribusikan dan diinstall
2. **Dependency Management**: Dependensi dikelola secara eksplisit
3. **Entry Points**: Dapat dijalankan dari command line
4. **Testing**: Mudah di-test sebagai paket terpisah
5. **Reusability**: Kode dapat di-reuse di aplikasi lain

### Perbedaan dengan Single-File:
- **Struktur**: Terorganisir dalam paket dengan modul terpisah
- **Konfigurasi**: Menggunakan file .ini untuk settings
- **Deployment**: Lebih mudah di-deploy dan di-manage
- **Scalability**: Lebih mudah dikembangkan menjadi aplikasi kompleks

### Konsep Penting:
1. **Entry Points**: Fungsi main sebagai titik masuk aplikasi
2. **Configuration Files**: .ini files untuk settings aplikasi
3. **Package Structure**: Struktur direktori Python standar
4. **Auto-scanning**: Pyramid dapat auto-discover views

### Workflow Development:
1. Setup paket dengan setup.py
2. Buat struktur direktori
3. Implement views dan konfigurasi
4. Test dengan pserve
5. Deploy sebagai egg

## Kesimpulan
Tutorial ini menunjukkan evolusi dari single-file ke packaged application, memberikan fondasi untuk development aplikasi Pyramid yang lebih kompleks dan maintainable.
