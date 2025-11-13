# Tutorial 12: Template dengan Jinja2

## Gambaran Umum

Tutorial ini memperkenalkan penggunaan **Jinja2 templating** dalam aplikasi Pyramid, yang membantu memisahkan logika presentasi (tampilan) dari logika aplikasi menggunakan sistem rendering template yang kuat.

## Konsep Utama

### Mesin Template

**Jinja2** adalah mesin template modern dan cepat untuk Python.

### Rendering Template

Menjelaskan bagaimana Pyramid berintegrasi dengan Jinja2 untuk menghasilkan halaman HTML secara dinamis.

### Variabel Template

Menunjukkan cara mengirim data dari fungsi **view** ke template.

## Detail Implementasi

### Konfigurasi

```python
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
```

### Konfigurasi View

```python
@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return {'name': 'Home View'}
```

### Sintaks Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Home - {{ name }}</title>
</head>
<body>
    <h1>Welcome to {{ name }}</h1>
</body>
</html>
```

## Fitur Template

### Interpolasi Variabel

Menyisipkan nilai variabel Python ke dalam template HTML.

### Struktur Kontrol

* `{% if %}` untuk kondisi
* `{% for %}` untuk perulangan
* `{% set %}` untuk mendefinisikan variabel

### Filter

Mengubah atau memformat nilai variabel dalam template.

### Pewarisan Template

Membuat **base template** dan menurunkannya ke halaman lain agar kode tidak berulang.

## Jinja2 vs Chameleon

### Perbandingan Sintaks

* Jinja2: `{{ variable }}`, `{% if %}`
* Chameleon: `${variable}`, `tal:condition`

### Performa

Keduanya cepat, tapi **Jinja2** biasanya lebih unggul untuk template yang kompleks.

### Fitur

Jinja2 memiliki lebih banyak filter dan fungsi bawaan.

### Ekosistem

Jinja2 lebih banyak digunakan di luar Pyramid (misalnya di Flask dan Django).

## Templating Lanjutan

### Macros

Mendefinisikan komponen template yang bisa digunakan berulang.

### Include

Menyertakan template lain di dalam satu template utama.

### Filter Kustom

Membuat filter sendiri untuk kebutuhan aplikasi tertentu.

### Konteks Template

Mengatur variabel dan ruang lingkup data yang dikirim ke template.

## Organisasi Template

### Struktur Direktori

Template disusun secara logis dalam folder seperti `templates/`.

### Konvensi Penamaan

Gunakan nama template yang konsisten dan deskriptif.

### Manajemen Aset

Menghubungkan CSS, JavaScript, dan gambar dalam template.

### Cache Template

Meningkatkan performa dengan menyimpan hasil kompilasi template.

## Analisis

### Pemisahan Tanggung Jawab

Memisahkan logika tampilan dari logika aplikasi membuat kode lebih bersih.

### Kemudahan Pemeliharaan

Template yang terpisah lebih mudah dikelola dan diperbarui.

### Reusabilitas

Template bisa digunakan ulang di berbagai halaman atau view.

### Pertimbangan Performa

Gunakan caching dan hindari template yang terlalu kompleks.

### Keamanan

Pastikan untuk mencegah **template injection** dan melakukan **escaping** pada input pengguna.

## Praktik Terbaik

### Struktur Template

* Gunakan struktur folder yang konsisten
* Buat template kecil dan fokus
* Gunakan nama variabel yang bermakna
* Tambahkan komentar untuk dokumentasi

### Pengiriman Variabel

* Hanya kirim data yang dibutuhkan
* Gunakan dictionary untuk data kompleks
* Hindari logika bisnis di template
* Selalu sanitasi input pengguna

### Pewarisan Template

* Gunakan base template untuk elemen umum (navbar, footer, dll.)
* Gunakan block untuk area yang bisa disesuaikan
* Jaga hierarki pewarisan tetap sederhana
* Dokumentasikan penggunaan tiap block

### Performa

* Aktifkan caching di mode produksi
* Kurangi kompleksitas template
* Gunakan filter dengan efisien
* Profil waktu render jika perlu

### Keamanan

* Escape input secara otomatis
* Gunakan filter `safe` dengan hati-hati
* Validasi data sebelum dirender
* Hindari eksekusi kode berbahaya di template

## Kesimpulan

Templating dengan **Jinja2** memungkinkan pengembang Pyramid untuk memisahkan tampilan dari logika bisnis, menghasilkan aplikasi yang lebih **terstruktur, aman, dan mudah dikelola**. Dengan memanfaatkan fitur seperti pewarisan, filter, dan macro, Jinja2 memberikan fleksibilitas tinggi dalam membangun antarmuka web yang dinamis dan efisien.
