

# Tutorial 16: Mengumpulkan Informasi Aplikasi Menggunakan Logging

## Gambaran Umum

Tutorial ini menjelaskan implementasi logging yang komprehensif dalam aplikasi Pyramid.
Melanjutkan dari *view classes* pada tutorial 15, di sini kamu akan belajar bagaimana cara **mengumpulkan, mengatur, dan memanfaatkan informasi aplikasi** melalui praktik logging yang terstruktur.
Kamu juga akan mempelajari cara menerapkan logging di berbagai level, melacak siklus hidup request, memantau performa, dan menangani error dengan efektif.

---

## Konsep Utama

### Dasar-dasar Logging Aplikasi

Memahami level, format, dan praktik terbaik logging dalam aplikasi web.

### Pelacakan Siklus Hidup Request

Logging di seluruh siklus request-response.

### Pemantauan Performa

Mengukur dan mencatat waktu respon serta penggunaan sumber daya.

### Penanganan Error dan Debugging

Pencatatan error yang lengkap serta pengumpulan informasi debugging.

### Logging Terstruktur

Format log yang konsisten dengan informasi kontekstual.

---

## Detail Implementasi

### Konfigurasi Logging

```python
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Konfigurasi ini menyiapkan infrastruktur logging dasar dengan format dan level yang seragam.
Setiap pesan log akan memiliki **timestamp**, nama logger, dan level keparahan (INFO, DEBUG, ERROR, dll).

---

### Integrasi Logger ke Request

```python
def get_logger(request):
    """Menambahkan logger ke objek request."""
    return logging.getLogger('tutorial')

# Di fungsi main:
config.add_request_method(get_logger, 'logger', reify=True)
```

Dengan menambahkan logger sebagai *request method*, kamu bisa mengakses logger dari mana saja dalam aplikasi.
Parameter `reify=True` memastikan logger hanya dibuat sekali per request.

---

### Logging di Level View

```python
@view_defaults(route_name='home', renderer='templates/home.html')
class HomeViews:
    def __init__(self, request):
        self.request = request
        self.logger = request.logger

    @view_config(request_method='GET')
    def home(self):
        self.logger.info(f"Halaman home diakses dari {self.request.remote_addr}")
        return {'title': 'Tutorial Logging', 'companies': list(COMPANIES.keys())}
```

Setiap *view class* menginisialisasi logger dan mencatat event penting, memberikan visibilitas terhadap pola penggunaan aplikasi dan membantu debugging.

---

### Logging Performa

```python
@view_config(request_method='GET')
def hello(self):
    start_time = time.time()
    self.logger.info(f"Halaman hello diminta untuk nama: {self.name}")

    result = {'name': self.name, 'greeting': f'Halo, {self.name}!'}

    end_time = time.time()
    self.logger.debug(f"Halaman hello dirender dalam {end_time - start_time:.4f} detik")

    return result
```

Bagian ini mencatat waktu eksekusi untuk memantau performa.
Gunakan `DEBUG` untuk informasi detail dan `INFO` untuk aktivitas umum.

---

### Logging Error

```python
@view_config(request_method='POST', renderer='json')
def hello_post(self):
    try:
        data = self.request.json_body
        return {'result': 'processed'}
    except Exception as e:
        self.logger.error(f"Kesalahan saat memproses POST request: {str(e)}")
        return {'error': 'Data request tidak valid', 'details': str(e)}
```

Semua error ditangkap dan dicatat bersama konteksnya, sehingga lebih mudah dilacak dan diperbaiki.

---

### Logging API

```python
@view_config(request_method='PUT', renderer='json')
def update_company(self):
    self.logger.info(f"PUT request untuk update perusahaan: {self.company_name}")

    try:
        update_data = self.request.json_body
        self.logger.debug(f"Data update diterima: {update_data}")
        return {'message': 'Perusahaan berhasil diperbarui'}
    except Exception as e:
        self.logger.error(f"Kesalahan saat update {self.company_name}: {str(e)}")
        return {'error': str(e)}
```

Operasi API mencatat keberhasilan maupun kegagalan, dengan level `DEBUG` untuk data detail.

---

## Level Logging dan Penggunaannya

### DEBUG

Digunakan untuk informasi diagnostik detail:

```python
self.logger.debug(f"Waktu proses: {end_time - start_time:.4f} detik")
```

### INFO

Digunakan untuk informasi umum:

```python
self.logger.info(f"Halaman home diakses dari {self.request.remote_addr}")
```

### WARNING

Digunakan untuk situasi yang berpotensi bermasalah:

```python
self.logger.warning(f"Perusahaan tidak ditemukan: {self.company_name}")
```

### ERROR

Untuk masalah serius:

```python
self.logger.error(f"Kesalahan saat memproses request: {str(e)}")
```

---

## Logging Konteks Request

### Metadata Request

```python
def debug_info(self):
    debug_data = {
        'method': self.request.method,
        'url': str(self.request.url),
        'params': dict(self.request.params),
        'headers': dict(self.request.headers),
        'remote_addr': self.request.remote_addr,
        'timestamp': datetime.now().isoformat()
    }
    self.logger.debug(f"Data debug dikumpulkan: {debug_data}")
    return debug_data
```

Log ini menyimpan informasi lengkap tiap request — berguna untuk debugging dan pemantauan keamanan.

---

### Pelacakan Aktivitas Pengguna

```python
@view_config(route_name='logs', renderer='templates/logs.html')
class LogViews:
    def __call__(self):
        self.logger.info("Halaman logs diakses")
        self.logger.debug("Ini pesan debug")
        self.logger.info("Ini pesan info")
        self.logger.warning("Ini pesan warning")
        self.logger.error("Ini pesan error")
```

Bagian ini menunjukkan penggunaan berbagai level logging untuk aktivitas pengguna.

---

## Pola Logging Terstruktur

### Format Pesan yang Konsisten

```python
self.logger.info(f"{self.request.method} {self.request.path} dari {self.request.remote_addr}")
self.logger.info(f"Perusahaan {self.company_name} berhasil diperbarui")
self.logger.error(f"Gagal memproses {operation}: {str(e)}")
```

### Informasi Kontekstual

```python
log_context = {
    'user_id': self.request.authenticated_userid,
    'session_id': self.request.session.get('id'),
    'request_id': getattr(self.request, 'id', 'unknown'),
    'timestamp': datetime.now().isoformat()
}
self.logger.info("Operasi selesai", extra=log_context)
```

---

## Pemantauan Performa

### Pelacakan Waktu Respon

```python
start_time = time.time()
result = self.process_request()
end_time = time.time()

response_time = end_time - start_time
self.logger.info(f"Request diproses dalam {response_time:.4f} detik")

if response_time > 1.0:
    self.logger.warning(f"Request lambat terdeteksi: {response_time:.4f} detik")
```

### Logging Penggunaan Resource

```python
import psutil
import os

def log_resource_usage(self):
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    cpu_percent = process.cpu_percent()

    self.logger.debug(f"Penggunaan memori: {memory_usage:.2f} MB, CPU: {cpu_percent:.1f}%")
```

---

## Pola Penanganan Error

### Try-Except dengan Logging

```python
try:
    data = self.request.json_body
    result = self.process_data(data)
    return {'success': True, 'result': result}
except json.JSONDecodeError as e:
    self.logger.warning(f"JSON tidak valid: {str(e)}")
    return {'error': 'Format JSON salah'}
except Exception as e:
    self.logger.error(f"Error tak terduga: {str(e)}", exc_info=True)
    return {'error': 'Kesalahan internal server'}
```

### Validasi Data dengan Logging

```python
def validate_company_data(self, data):
    errors = []
    if 'name' not in data:
        errors.append('name wajib diisi')
        self.logger.warning("Gagal membuat perusahaan: field name kosong")

    if errors:
        self.logger.error(f"Validasi gagal: {errors}")
        raise ValidationError(errors)
```

---

## Logging Keamanan

### Event Autentikasi

```python
def log_authentication(self, username, success):
    if success:
        self.logger.info(f"Login berhasil untuk user: {username}")
    else:
        self.logger.warning(f"Login gagal untuk user: {username} dari {self.request.remote_addr}")
```

### Kontrol Akses

```python
def check_permission(self, resource, action):
    if not self.has_permission(resource, action):
        self.logger.warning(f"Akses ditolak: {action} pada {resource} oleh {self.request.authenticated_userid}")
        raise HTTPForbidden()
```

---

## Analisis dan Pemantauan Log

### Agregasi Log

```python
def analyze_logs():
    # Hitung jumlah error per jam
    # Hitung request per endpoint
    # Deteksi request lambat
    # Deteksi pola tak biasa
```

### Sistem Peringatan (Alerting)

```python
def check_error_threshold():
    recent_errors = get_recent_errors()
    if len(recent_errors) > ERROR_THRESHOLD:
        self.logger.critical(f"Batas error terlampaui: {len(recent_errors)} error dalam 1 jam terakhir")
```

---

## Pengujian Logging

### Unit Test Log Output

```python
def test_logging():
    with mock.patch('logging.Logger.info') as mock_info:
        view = HomeViews(dummy_request)
        view.home()
        mock_info.assert_called_with("Halaman home diakses dari 127.0.0.1")
```

### Integration Test

```python
def test_request_logging(app):
    with mock.patch('logging.Logger.info') as mock_info:
        app.get('/')
        assert mock_info.called
        assert 'Halaman home diakses' in mock_info.call_args[0][0]
```

---

## Manajemen Konfigurasi

### Logging Berdasarkan Lingkungan

```python
import os

log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper())
logging.basicConfig(level=log_level)
```

### Konfigurasi Terstruktur (file INI)

```ini
[logger_tutorial]
level = DEBUG
handlers = console,file
qualname = tutorial

[handler_file]
class = FileHandler
args = ('app.log',)
formatter = detailed
```

---

## Praktik Terbaik

### Panduan Pesan Log

* Gunakan format yang konsisten
* Sertakan konteks yang relevan
* Jangan log data sensitif
* Gunakan level log yang sesuai

### Pertimbangan Performa

* Gunakan logging asynchronous jika memungkinkan
* Gunakan format terstruktur seperti JSON
* Terapkan log rotation
* Pantau ukuran file log

### Pertimbangan Keamanan

* Jangan log password atau data pribadi
* Bersihkan input pengguna sebelum dicatat
* Batasi akses file log
* Tinjau log secara rutin

---

## Analisis

### Keuntungan Logging yang Komprehensif

* **Debugging:** Mempermudah identifikasi dan penyelesaian masalah
* **Monitoring:** Memberi visibilitas terhadap kesehatan aplikasi
* **Keamanan:** Melacak aktivitas mencurigakan
* **Performa:** Mengidentifikasi bottleneck
* **Audit:** Membantu kepatuhan dan pelacakan

### Kelemahan

* Logging memakan sumber daya
* File log bisa cepat membesar
* Harus hati-hati agar tidak mencatat data pribadi

### Pola Implementasi

* Konfigurasi terpusat
* Propagasi konteks (request ID, user ID)
* Data log terstruktur (JSON)
* Penggunaan level log yang tepat

### Skalabilitas

* Agregasi log secara terpusat
* Logging asynchronous
* Rotasi otomatis log
* Kompresi log lama

---

## Kesimpulan

Logging yang menyeluruh sangat penting untuk aplikasi web modern.
Tutorial ini menunjukkan cara menerapkan logging di seluruh bagian aplikasi Pyramid, mulai dari pelacakan request hingga pemantauan performa dan penanganan error.

Dengan praktik logging yang baik, pengembang bisa membangun sistem yang **lebih kuat, aman, mudah dipantau, dan mudah dipelihara**.

--
