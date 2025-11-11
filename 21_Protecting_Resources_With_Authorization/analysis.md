# 21: Melindungi Sumber Daya Dengan Otorisasi

Tutorial ini mendemonstrasikan cara melindungi sumber daya dalam aplikasi Pyramid menggunakan otorisasi berdasarkan peran dan izin pengguna.

## Tujuan

- Mengimplementasikan kontrol akses berbasis peran (RBAC)
- Melindungi berbagai view dengan tingkat izin yang berbeda
- Membuat callback groupfinder untuk menetapkan grup berdasarkan peran pengguna
- Menangani upaya akses terlarang dengan baik
- Mendemonstrasikan perbedaan antara autentikasi dan otorisasi

## Konsep Kunci

### Autentikasi vs Otorisasi

- **Autentikasi**: Memverifikasi siapa pengguna tersebut (ditangani di tutorial 20)
- **Otorisasi**: Menentukan apa yang dapat dilakukan pengguna yang terautentikasi (tutorial ini)

### Access Control Lists (ACLs)

ACL mendefinisikan izin untuk sumber daya. Setiap entri ACL adalah tuple dari:
1. Aksi (Allow atau Deny)
2. Principal (pengguna, grup, atau identifier khusus seperti Everyone atau Authenticated)
3. Izin (string seperti 'view', 'edit', 'admin')

## Langkah-langkah Implementasi

### Langkah 1: Memperbarui Model User

Kami menambahkan field `role` ke model User untuk menyimpan peran pengguna:

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    password = Column(String(100))
    role = Column(String(50), default='viewer')  # viewer, editor, admin
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_modified = Column(DateTime(timezone=True), default=func.now())
```

### Langkah 2: Membuat Callback Groupfinder

Callback groupfinder memetakan pengguna ke grup berdasarkan peran mereka:

```python
def groupfinder(userid, request):
    """
    Mengembalikan grup (peran) untuk pengguna tertentu.
    Callback ini digunakan oleh kebijakan autentikasi.
    """
    user = DBSession.query(User).filter_by(name=userid).first()
    if user:
        if user.role == 'admin':
            return ['group:admins', 'group:editors']
        elif user.role == 'editor':
            return ['group:editors']
    return []
```

Poin penting:
- Admin mendapatkan grup 'group:admins' dan 'group:editors'
- Editor hanya mendapatkan grup 'group:editors'
- Viewer tidak mendapatkan grup (list kosong)

### Langkah 3: Memperbarui ACL Root Factory

RootFactory mendefinisikan ACL default untuk aplikasi:

```python
class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit'),
        (Allow, 'group:editors', 'edit'),
        (Allow, 'group:admins', 'admin'),
    ]
```

ACL ini berarti:
- Semua orang (termasuk pengguna anonim) dapat 'view'
- Pengguna terautentikasi dapat 'edit'
- Pengguna dalam 'group:editors' dapat 'edit'
- Pengguna dalam 'group:admins' dapat 'admin'

### Langkah 4: Mengkonfigurasi Kebijakan Keamanan

Di `__init__.py`, kami mengkonfigurasi kebijakan autentikasi dengan callback groupfinder:

```python
authn_policy = AuthTktAuthenticationPolicy(
    settings['tutorial.secret'], 
    callback=groupfinder,  # Ini adalah penambahan kunci
    hashalg='sha512',
)
authz_policy = ACLAuthorizationPolicy()
config.set_authentication_policy(authn_policy)
config.set_authorization_policy(authz_policy)
```

Kami juga mengatur root_factory:

```python
config = Configurator(settings=settings, root_factory=RootFactory)
```

### Langkah 5: Melindungi View dengan Izin

Setiap view dapat menentukan izin yang diperlukan:

```python
@view_config(route_name='home', permission='view')
def home(self):
    # Semua orang dapat mengakses ini

@view_config(route_name='editor', permission='edit')
def editor(self):
    # Hanya editor dan admin yang dapat mengakses ini

@view_config(route_name='admin', permission='admin')
def admin(self):
    # Hanya admin yang dapat mengakses ini
```

### Langkah 6: Menangani Akses Terlarang

Kami membuat view forbidden yang menangani upaya akses tidak sah:

```python
@forbidden_view_config(renderer='forbidden.html')
def forbidden_view(request):
    login_url = request.route_url('login', _query={'came_from': request.url})
    if not request.authenticated_userid:
        # Pengguna tidak login, redirect ke halaman login
        return HTTPFound(location=login_url)
    
    # Pengguna login tetapi tidak memiliki izin
    return {
        'name': 'Forbidden',
        'message': 'Anda tidak memiliki izin untuk mengakses sumber daya ini.',
        'login_url': login_url,
    }
```

View ini:
- Mengarahkan pengguna yang tidak terautentikasi ke halaman login
- Menampilkan halaman forbidden untuk pengguna terautentikasi tanpa izin

### Langkah 7: Inisialisasi Database dengan Beberapa Pengguna

Script initialize_db membuat tiga pengguna uji dengan peran berbeda:

```python
# Membuat pengguna admin
admin = User(
    name='admin', 
    password=hash_password('admin'), 
    email='admin@example.com',
    role='admin'
)

# Membuat pengguna editor
editor = User(
    name='editor', 
    password=hash_password('editor'), 
    email='editor@example.com',
    role='editor'
)

# Membuat pengguna viewer
viewer = User(
    name='viewer', 
    password=hash_password('viewer'), 
    email='viewer@example.com',
    role='viewer'
)
```

### Langkah 8: Membuat Template Khusus Peran

Kami membuat template untuk tingkat akses yang berbeda:
- `home.html`: Dapat diakses oleh semua orang
- `editor.html`: Dapat diakses oleh editor dan admin
- `admin.html`: Hanya dapat diakses oleh admin
- `forbidden.html`: Ditampilkan ketika akses ditolak

## Menguji Otorisasi

Untuk menguji aplikasi:

1. Install dependensi:
   ```bash
   cd 21_Protecting_Resources_With_Authorization
   pip install -e .
   ```

2. Inisialisasi database:
   ```bash
   initialize_tutorial_db development.ini
   ```

3. Jalankan aplikasi:
   ```bash
   pserve development.ini
   ```

4. Uji dengan pengguna berbeda:
   - Login sebagai `viewer` (password: `viewer`):
     - Dapat mengakses: Halaman Home
     - Tidak dapat mengakses: Halaman Editor, Halaman Admin
   
   - Login sebagai `editor` (password: `editor`):
     - Dapat mengakses: Halaman Home, Halaman Editor
     - Tidak dapat mengakses: Halaman Admin
   
   - Login sebagai `admin` (password: `admin`):
     - Dapat mengakses: Semua halaman (Home, Editor, Admin)

## Alur Otorisasi

1. Pengguna mencoba mengakses sumber daya yang dilindungi
2. Pyramid memeriksa apakah pengguna terautentikasi
3. Jika terautentikasi, Pyramid memanggil groupfinder untuk mendapatkan grup pengguna
4. Pyramid memeriksa ACL untuk melihat apakah ada grup pengguna yang memiliki izin yang diperlukan
5. Jika izin diberikan, view dieksekusi
6. Jika izin ditolak, view forbidden dipanggil

## Praktik Terbaik Keamanan

1. **Prinsip Hak Istimewa Terkecil**: Berikan pengguna hanya izin yang mereka butuhkan
2. **Defense in Depth**: Gunakan beberapa lapisan keamanan (autentikasi + otorisasi)
3. **Fail Securely**: Default untuk menolak akses kecuali secara eksplisit diizinkan
4. **Audit Trail**: Catat upaya akses (terutama yang gagal)
5. **Review Berkala**: Tinjau dan perbarui izin secara berkala

## Perbedaan Utama dari Tutorial 20

Tutorial 20 (Autentikasi):
- Fokus pada verifikasi identitas pengguna
- Mengimplementasikan fungsi login/logout
- Menggunakan pemeriksaan izin dasar

Tutorial 21 (Otorisasi):
- Fokus pada kontrol akses berdasarkan peran
- Mengimplementasikan kontrol akses berbasis peran
- Membuat beberapa tingkat izin
- Menambahkan callback groupfinder
- Menangani akses terlarang dengan baik

## Analisis

Tutorial ini mendemonstrasikan sistem kontrol akses berbasis peran yang lengkap di Pyramid. Komponen kuncinya adalah:

1. **Peran Pengguna**: Disimpan dalam database (admin, editor, viewer)
2. **Grup**: Ditetapkan secara dinamis melalui callback groupfinder
3. **Izin**: Didefinisikan dalam ACL (view, edit, admin)
4. **Perlindungan**: Diterapkan pada view melalui parameter permission
5. **Penanganan Error**: Penanganan akses tidak sah yang baik

Sistem ini fleksibel dan dapat diperluas untuk mendukung:
- Izin yang lebih granular
- ACL tingkat sumber daya (izin berbeda untuk objek berbeda)
- Penetapan izin dinamis
- Pewarisan izin
- Aturan otorisasi yang kompleks

## Pola Umum

### Pola 1: Peran Hierarkis
Admin mewarisi izin editor dengan ditetapkan ke kedua grup:
```python
if user.role == 'admin':
    return ['group:admins', 'group:editors']
```

### Pola 2: Otorisasi Berbasis Konteks
Sumber daya yang berbeda dapat memiliki ACL yang berbeda dengan menggunakan context factories alih-alih single root factory.

### Pola 3: Pemeriksaan Izin dalam Template
Template dapat memeriksa izin untuk menampilkan/menyembunyikan elemen UI secara kondisional:
```jinja2
{% if request.has_permission('edit') %}
    <a href="/editor">Halaman Editor</a>
{% endif %}
```

## Kesimpulan

Tutorial ini melengkapi cerita autentikasi dan otorisasi di Pyramid. Bersama dengan tutorial 20, ini memberikan fondasi keamanan lengkap untuk aplikasi web, mendemonstrasikan cara:
- Memverifikasi identitas pengguna (autentikasi)
- Mengontrol akses ke sumber daya (otorisasi)
- Mengimplementasikan kontrol akses berbasis peran
- Menangani error keamanan dengan baik
- Membuat aplikasi yang aman dan ramah pengguna