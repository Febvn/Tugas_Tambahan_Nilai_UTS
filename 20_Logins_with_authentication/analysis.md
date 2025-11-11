# 20: Login dengan Autentikasi

Tutorial ini memperkenalkan autentikasi dan otorisasi dalam Pyramid.

## Tujuan

- Menambahkan autentikasi ke aplikasi Pyramid
- Menambahkan otorisasi ke aplikasi Pyramid
- Menggunakan database untuk menyimpan kredensial pengguna
- Menggunakan password terenkripsi

## Langkah-langkah

### Langkah 1: Menambahkan kebijakan autentikasi dan otorisasi

Kami menambahkan kebijakan autentikasi dan otorisasi ke configurator di `__init__.py`:

```python
# Kebijakan keamanan
authn_policy = AuthTktAuthenticationPolicy(
    settings['tutorial.secret'], hashalg='sha512',
)
authz_policy = ACLAuthorizationPolicy()
config.set_authentication_policy(authn_policy)
config.set_authorization_policy(authz_policy)
```

### Langkah 2: Menambahkan root factory dengan ACL

Kami membuat `RootFactory` di `security.py` yang mendefinisikan ACL yang memungkinkan semua orang untuk view, tetapi hanya editors untuk edit:

```python
class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:editors', 'edit'),
    ]
```

### Langkah 3: Menambahkan model user dan setup database

Kami menambahkan model `User` di `models.py` dengan field untuk name, email, phone, password, dan timestamps.

Kami juga menambahkan script inisialisasi di `scripts/initialize_db.py` yang membuat pengguna default.

### Langkah 4: Menambahkan utilities keamanan

Kami menambahkan fungsi hashing dan checking password di `security.py` menggunakan bcrypt.

### Langkah 5: Menambahkan views login dan logout

Kami menambahkan views login dan logout di `views.py` yang menangani autentikasi.

### Langkah 6: Menambahkan templates

Kami menambahkan template `home.html` dan `login.html` untuk user interface.

### Langkah 7: Menambahkan static assets

Kami menambahkan file CSS dan JS untuk styling dan fungsionalitas client-side.

## Analisis

Tutorial ini mendemonstrasikan cara menambahkan autentikasi dan otorisasi ke aplikasi Pyramid. Tutorial ini menggunakan SQLAlchemy untuk penyimpanan user, bcrypt untuk hashing password, dan kebijakan keamanan built-in Pyramid.

Aplikasi sekarang memerlukan pengguna untuk login untuk mengakses resource yang dilindungi, dan pengguna yang berbeda dapat memiliki izin yang berbeda berdasarkan keanggotaan grup mereka.