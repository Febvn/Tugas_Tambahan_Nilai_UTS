# Analisis: 03 - Application Configuration with .ini Files

## Deskripsi Tutorial
Tutorial ini menunjukkan bagaimana menggunakan file konfigurasi .ini untuk mengelola settings aplikasi Pyramid, termasuk konfigurasi untuk development dan production environment.

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
- Setup paket Python standar dengan dependensi Pyramid

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
- Fungsi main sebagai entry point aplikasi
- Menggunakan Configurator dengan settings dari .ini file
- Menambahkan dua routes: home (/) dan hello (/howdy)

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
- Dua view functions dengan string renderer
- Route home mengembalikan "Welcome!"
- Route hello mengembalikan "Hello!"

### development.ini dan production.ini
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
- Port default 6543 untuk kedua environment

## Cara Menjalankan
1. Install paket: `pip install -e .`
2. Jalankan development: `pserve development.ini`
3. Jalankan production: `pserve production.ini`
4. Akses:
   - http://localhost:6543 (Welcome!)
   - http://localhost:6543/howdy (Hello!)

## Analisis Teknis

### Keuntungan File Konfigurasi .ini:
1. **Environment Separation**: Development vs Production settings
2. **Deployment Flexibility**: Mudah mengubah konfigurasi tanpa kode
3. **Security**: Sensitive data dapat dipisahkan dari kode
4. **Maintainability**: Konfigurasi terpusat dan mudah diubah

### Struktur File .ini:
- **[app:main]**: Konfigurasi aplikasi utama
- **[server:main]**: Konfigurasi server WSGI
- **use = egg:tutorial**: Menggunakan entry point dari paket

### Perbedaan dengan Tutorial Sebelumnya:
- **Multiple Routes**: Menambahkan route kedua (/howdy)
- **Configuration Files**: Memisahkan konfigurasi dari kode
- **Environment Aware**: Mendukung development dan production

### Konsep Penting:
1. **Configuration Management**: Settings dikelola melalui file eksternal
2. **Entry Points**: Aplikasi dapat dijalankan sebagai egg
3. **Route Configuration**: Routes didefinisikan dalam kode Python
4. **Renderer Types**: Menggunakan string renderer untuk response sederhana

### Workflow Development:
1. Buat file konfigurasi untuk setiap environment
2. Implement routes dan views dalam kode
3. Test dengan pserve menggunakan file .ini yang berbeda
4. Deploy dengan konfigurasi yang sesuai environment

## Kesimpulan
Tutorial ini memperkenalkan konsep konfigurasi aplikasi yang penting untuk development dan deployment Pyramid yang professional, memungkinkan separation of concerns antara kode dan konfigurasi.
