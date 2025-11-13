# Tutorial 19: Database Menggunakan SQLAlchemy

## Gambaran Umum

Tutorial ini menjelaskan cara mengintegrasikan **SQLAlchemy**, sebuah pustaka **Object-Relational Mapping (ORM)** yang kuat, ke dalam aplikasi **Pyramid**. Materi mencakup **setup database**, **definisi model**, **manajemen sesi (session)**, dan **operasi CRUD**, memberikan dasar yang kuat untuk membangun aplikasi web berbasis data.

---

## Konsep Utama

### SQLAlchemy ORM

Memahami **Object-Relational Mapping (ORM)** dan bagaimana cara kerjanya menyederhanakan interaksi dengan database.

### Model Database

Mendefinisikan **kelas Python** yang dipetakan ke tabel-tabel dalam database.

### Manajemen Sesi

Mengatur koneksi dan transaksi antara aplikasi dan database.

### Operasi CRUD

Mengimplementasikan operasi **Create, Read, Update, Delete** pada data.

### Inisialisasi Database

Membuat dan mengisi **skema database** untuk pertama kali.

---

## Detail Implementasi

### Definisi Model SQLAlchemy

```python
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', backref='pages')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    email = Column(Text, unique=True)
```

Model di atas mendefinisikan **struktur tabel database** menggunakan sintaks deklaratif SQLAlchemy. Hubungan antar tabel ditentukan dengan fungsi `relationship()` dan `ForeignKey`.

---

### Konfigurasi Sesi Database

```python
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
```

`ZopeTransactionExtension` mengintegrasikan sesi SQLAlchemy dengan **manajemen transaksi Pyramid**, sehingga proses **commit** dan **rollback** dilakukan secara otomatis dan aman.

---

### Skrip Inisialisasi Database

```python
def main(argv=sys.argv):
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    Base.metadata.create_all(engine)
```

Skrip inisialisasi ini membuat semua tabel yang didefinisikan di dalam model dan dapat digunakan untuk mengisi data awal ke dalam database.

---

### Fungsi View dengan Operasi Database

```python
@view_config(route_name='page', renderer='templates/page.html')
def page_view(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        raise HTTPNotFound('No such page')

    return dict(page=page, user=get_user(request))

@view_config(route_name='add_page', renderer='templates/edit.html', permission='edit')
def add_page_view(request):
    pagename = request.matchdict['pagename']
    if 'form.submitted' in request.params:
        body = request.params['body']
        page = Page(name=pagename, data=body)
        page.creator_id = get_user(request).id
        DBSession.add(page)
        return HTTPFound(location=request.route_url('page', pagename=pagename))
```

Fungsi view ini melakukan **query dan modifikasi data** menggunakan sesi database yang sudah dikonfigurasi.

---

## Analisis

### Keuntungan Integrasi SQLAlchemy

* **Abstraksi**: Operasi database dilakukan melalui objek Python, bukan SQL mentah.
* **Portabilitas**: Kode dapat bekerja di berbagai jenis database tanpa perubahan besar.
* **Produktivitas**: Mengurangi kode SQL berulang.
* **Kemudahan Pemeliharaan**: Perubahan struktur database tercermin dalam kode model.
* **Performa**: Query dijalankan secara efisien oleh SQLAlchemy.

---

### Manajemen Sesi Database

* **Scoped Sessions**: Setiap thread memiliki sesi sendiri untuk menghindari konflik data.
* **Integrasi Transaksi**: Commit dan rollback dilakukan otomatis bersama transaksi Pyramid.
* **Connection Pooling**: Koneksi database digunakan kembali untuk efisiensi.
* **Lazy Loading**: Data relasi hanya diambil saat dibutuhkan.

---

### Pertimbangan Keamanan

* **Validasi Input**: Semua data dari pengguna harus divalidasi sebelum disimpan.
* **Perlindungan SQL Injection**: SQLAlchemy secara otomatis men-escape parameter.
* **Pemeriksaan Izin (Permission Check)**: Operasi database harus mematuhi aturan otorisasi.
* **Sanitasi Data**: Data pengguna perlu disaring sebelum disimpan.

---

### Optimasi Performa

* **Optimasi Query**: Gunakan `selectinload` atau `joinedload` untuk memuat relasi dengan efisien.
* **Indexing**: Tambahkan indeks pada kolom yang sering digunakan untuk pencarian.
* **Caching**: Terapkan sistem cache untuk data yang sering diakses.
* **Pagination**: Batasi hasil query untuk dataset besar.

---

### Praktik Terbaik

* **Pemisahan Model dan Logika Bisnis**: Jangan campur logika aplikasi dalam model.
* **Migrasi Database**: Gunakan **Alembic** untuk menangani perubahan struktur database.
* **Pengujian**: Gunakan database in-memory untuk unit testing.
* **Konfigurasi Koneksi**: Simpan URL database di file konfigurasi, bukan di kode.
* **Penanganan Error**: Tangani kesalahan database dengan baik untuk mencegah crash.

---

## Kesimpulan

**SQLAlchemy** memberikan cara yang kuat dan fleksibel untuk bekerja dengan database di dalam aplikasi **Pyramid**. Dengan mengubah operasi database menjadi objek Python, proses pengembangan menjadi lebih mudah dan terstruktur. Pemahaman tentang pola dan praktik terbaik SQLAlchemy membantu menciptakan aplikasi berbasis data yang **stabil, skalabel, dan mudah dirawat**.
Manajemen sesi dan transaksi yang tepat memastikan **integritas data** dan **keandalan aplikasi**.
