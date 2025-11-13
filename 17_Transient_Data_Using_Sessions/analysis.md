

# Tutorial 17: Data Sementara Menggunakan Session

## Gambaran Umum

Tutorial ini menjelaskan cara menggunakan **session** di aplikasi web Pyramid untuk menyimpan **data sementara** yang tetap ada di antara beberapa permintaan (request) dari pengguna yang sama.
Session sangat penting untuk mempertahankan status pengguna, membuat sistem login, keranjang belanja, dan fitur lain yang memerlukan penyimpanan data antar kunjungan halaman.

---

## Konsep Utama

### Apa itu Session?

Session menyediakan cara untuk menyimpan data yang bertahan di antara beberapa permintaan HTTP dari klien yang sama.
Berbeda dengan cookie, data session disimpan di sisi server sehingga **lebih aman** untuk informasi sensitif.

### Jenis-jenis Session di Pyramid

1. **Signed Cookie Sessions** – Data disimpan di cookie yang ditandatangani pada sisi klien.
2. **Server-side Sessions** – Data disimpan di server (perlu konfigurasi tambahan).
3. **Database Sessions** – Data disimpan di database.

Tutorial ini menggunakan **Signed Cookie Session**, karena jenis ini paling umum dan menjadi default di Pyramid.

---

## Detail Implementasi

### Konfigurasi Aplikasi

Session factory diatur dalam file `tutorial/__init__.py`:

```python
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config = Configurator(settings=settings, session_factory=my_session_factory)
```

---

### Operasi pada Session

#### Menyimpan Data

```python
session = request.session
session['username'] = 'john_doe'
session['login_time'] = str(request.datetime)
```

#### Mengambil Data

```python
username = session.get('username')
counter = session.get('counter', 0)
```

#### Mengecek Kunci

```python
if 'username' in session:
    # User sudah login
```

#### Menghapus Data

```python
del session['username']
```

#### Menghapus Seluruh Session

```python
session.invalidate()
```

---

### Flash Messages

Flash message adalah pesan sementara yang disimpan dalam session, akan ditampilkan sekali, lalu otomatis dihapus:

```python
request.session.flash('Selamat datang!', 'success')
request.session.flash('Terjadi kesalahan', 'error')

# Di template
{% for message in request.session.pop_flash() %}
<div class="flash-{{ message.category }}">{{ message }}</div>
{% endfor %}
```

---

## Fitur yang Diterapkan

### 1. Autentikasi Pengguna

* Form login dengan input username
* Autentikasi berbasis session
* Fitur login/logout
* Pesan sambutan menggunakan flash message

### 2. Persistensi Data Session

* Menyimpan username di antara permintaan
* Mencatat waktu login
* Counter yang meningkat setiap kali halaman dimuat

### 3. Sistem Flash Message

* Beberapa kategori pesan (info, success, warning, error)
* Pesan otomatis dihapus setelah ditampilkan
* Tampilan pesan yang rapi

### 4. AJAX Counter

* Counter di sisi klien menggunakan `fetch API`
* Nilai counter disimpan di session server
* Pembaruan UI secara real-time

### 5. Tampilan Informasi Session

* Menampilkan data session saat ini
* Daftar kunci (keys) dalam session
* Menampilkan ID session (jika tersedia)

---

## Pertimbangan Keamanan

### Keamanan Session

* Session menggunakan cookie yang ditandatangani untuk mencegah manipulasi
* Kunci rahasia harus **kuat dan unik** untuk setiap aplikasi
* Data dalam cookie terenkripsi tapi tetap dapat dilihat pengguna (jangan simpan data sensitif)

### Praktik Terbaik

* Gunakan **HTTPS** di produksi agar cookie aman
* Terapkan **session timeout**
* Validasi data session di setiap request
* Gunakan **server-side session** untuk aplikasi produksi yang besar

---

## Fitur Template

### Template Jinja2

* Konten dinamis tergantung status session
* Tampilkan tombol login/logout secara kondisional
* Render flash message
* Visualisasi data session

### Aset Statis

* CSS untuk tampilan manajemen session
* JavaScript untuk fitur interaktif
* Desain responsif untuk tampilan mobile

---

## Routes dan Views

### Routes

* `/` — Halaman utama dengan info session
* `/login` — Form login (GET) dan proses login (POST)
* `/logout` — Fungsi logout
* `/counter` — Endpoint AJAX untuk counter
* `/flash` — Demo flash message

### View Functions

* `home()` — Menampilkan status session saat ini
* `login_form()` — Menampilkan form login
* `login_submit()` — Memproses login
* `logout()` — Menghapus session dan redirect
* `counter()` — Menambah nilai counter dan mengembalikan nilainya
* `flash_demo()` — Menampilkan demo flash message

---

## Pengujian Aplikasi

1. **Jalankan aplikasi**

   ```bash
   cd 17_Transient_Data_Using_Sessions
   pserve development.ini
   ```

2. **Uji fitur login**

   * Kunjungi `http://localhost:6543/`
   * Klik “Login” dan masukkan username
   * Pastikan data session tampil di halaman

3. **Uji counter**

   * Klik tombol “Increment Counter”
   * Lihat nilai counter berubah

4. **Uji flash message**

   * Buka halaman flash demo
   * Refresh untuk melihat berbagai jenis pesan

5. **Uji logout**

   * Klik “Logout”
   * Pastikan session terhapus

---

## Fitur Session Lanjutan

### Waktu Kedaluwarsa Session

```python
my_session_factory = SignedCookieSessionFactory(
    'itsaseekreet',
    timeout=3600  # 1 jam
)
```

### Serialisasi Session Kustom

```python
import json

class CustomSession(dict):
    def __init__(self, request):
        self.request = request
        super().__init__()

my_session_factory = SignedCookieSessionFactory(
    'itsaseekreet',
    cookie_name='myapp_session',
    max_age=3600,
    secure=True,   # hanya lewat HTTPS
    httponly=True  # tidak bisa diakses lewat JavaScript
)
```

### Server-side Session

Untuk aplikasi yang butuh keamanan lebih atau data session yang besar:

```python
from pyramid.session import UnencryptedCookieSessionFactoryConfig

# Konfigurasi server-side session butuh setup tambahan
# misalnya dengan database atau Redis
```

---

## Contoh Penggunaan Umum

1. **Autentikasi Pengguna** – Menyimpan ID pengguna dan status login
2. **Keranjang Belanja** – Menyimpan isi keranjang antar halaman
3. **Data Form** – Menyimpan data form di proses bertahap
4. **Preferensi Pengguna** – Menyimpan pengaturan pengguna
5. **Flash Message** – Menampilkan notifikasi sekali tampil
6. **Perlindungan CSRF** – Menyimpan token validasi form

---

## Pertimbangan Performa

* Signed cookie session menyimpan data di klien → **beban server lebih ringan**
* Namun, data session dikirim setiap request/response
* Data session yang besar bisa memperlambat aplikasi
* Gunakan server-side session untuk aplikasi besar

---

## Kesimpulan

Session adalah bagian penting dari aplikasi web modern, memungkinkan interaksi **stateful** di atas protokol HTTP yang **stateless**.
Tutorial ini menjelaskan konsep dasar dan implementasi praktis session di Pyramid, termasuk operasi dasar dan fitur lanjutan seperti flash message.

Dengan memahami cara kerja session, kamu bisa membangun aplikasi web interaktif yang mempertahankan status pengguna secara aman dan efisien.

---

Apakah kamu ingin saya lanjut bantu terjemahkan **Tutorial 18 (Form Handling)** juga biar satu set lengkap sebelum masuk ke SQLAlchemy?
