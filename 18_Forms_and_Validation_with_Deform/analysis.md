# Tutorial 18: Formulir dan Validasi dengan Deform

## Gambaran Umum

Tutorial ini menjelaskan cara membuat **form web yang kuat dan aman** menggunakan **Deform**, yaitu pustaka Python untuk pembuatan formulir HTML yang dibangun di atas **Colander** (pustaka untuk validasi dan deserialisasi data).
Deform menyediakan solusi lengkap untuk **pembuatan formulir**, **validasi data**, dan **rendering tampilan** dalam aplikasi Pyramid.

---

## Konsep Utama

### Apa itu Deform?

**Deform** adalah pustaka Python untuk menghasilkan formulir HTML dari skema yang didefinisikan menggunakan **Colander**.
Fitur utamanya:

* **Pembuatan form berbasis skema** – form dibuat dari definisi Python, bukan HTML manual
* **Validasi otomatis** – tersedia validasi sisi klien dan sisi server
* **Sistem widget** – berbagai elemen input seperti teks, checkbox, select, dan lainnya
* **Integrasi Bootstrap** – mendukung tampilan responsif berbasis CSS Bootstrap
* **Arsitektur yang mudah diperluas** – bisa menambah widget atau validator kustom

---

### Sistem Skema Colander

**Colander** berfungsi untuk validasi dan deserialisasi data.
Komponennya meliputi:

* **Schema nodes**: menentukan tipe data dan aturan validasi
* **Validators**: fungsi bawaan atau kustom untuk memeriksa validitas input
* **Serialization/Deserialization**: mengubah data antara objek Python dan format eksternal (seperti form input)
* **Penanganan error**: memberikan laporan kesalahan yang detail dan mudah dipahami

---

## Detail Implementasi

### Konfigurasi Aplikasi

Menambahkan sumber daya statis dan renderer untuk Jinja2:

```python
config.add_static_view('deform_static', 'deform:static/')
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
```

---

### Definisi Skema

#### Skema Formulir Kontak

```python
class Contact(colander.MappingSchema):
    name = colander.SchemaNode(
        colander.String(),
        title="Name",
        description="Your full name",
        validator=colander.Length(min=2, max=100)
    )
    email = colander.SchemaNode(
        colander.String(),
        title="Email",
        description="Your email address",
        validator=colander.Email()
    )
    message = colander.SchemaNode(
        colander.String(),
        title="Message",
        description="Your message",
        widget=deform.widget.TextAreaWidget(rows=10),
        validator=colander.Length(min=10, max=1000)
    )
```

Formulir ini meminta nama, email, dan pesan, dengan validasi panjang teks dan format email.

---

#### Skema Registrasi Pengguna

```python
class User(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Full Name", validator=colander.Length(min=3, max=100))
    age = colander.SchemaNode(colander.Integer(), title="Age", validator=colander.Range(min=13, max=120))
    email = colander.SchemaNode(colander.String(), validator=colander.Email())
    password = colander.SchemaNode(colander.String(), validator=colander.Length(min=8), widget=deform.widget.PasswordWidget())
    confirm_password = colander.SchemaNode(colander.String(), widget=deform.widget.PasswordWidget())

    def validator(self, node, cstruct):
        if cstruct.get('password') != cstruct.get('confirm_password'):
            raise colander.Invalid(node, "Passwords do not match")
```

Formulir ini memiliki validasi tambahan untuk memastikan password dan konfirmasi password cocok.

---

#### Skema Formulir Urutan (Sequence Form)

```python
class SequenceItem(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Name")
    value = colander.SchemaNode(colander.Integer(), title="Value")

class SequenceForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), title="Form Title")
    items = colander.SchemaNode(
        colander.Sequence(),
        SequenceItem(),
        title="Items",
        widget=deform.widget.SequenceWidget(min_len=1, max_len=10)
    )
```

Formulir ini mendukung daftar dinamis dengan tombol tambah/hapus item.

---

### Pemrosesan Formulir

#### Penanganan Dasar Formulir

```python
@view_config(route_name='contact', renderer='templates/contact.html')
def contact(request):
    schema = Contact()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            request.session.flash("Thank you for your message!", 'success')
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render()}

    return {'form': form.render()}
```

Kode ini memvalidasi input, menampilkan pesan sukses, atau mengembalikan pesan error jika validasi gagal.

---

## Jenis Widget

* **Input teks**: `TextInputWidget`, `TextAreaWidget`, `PasswordWidget`, `HiddenWidget`
* **Pilihan (select/radio/checkbox)**: `SelectWidget`, `RadioChoiceWidget`, `CheckboxChoiceWidget`, `CheckboxWidget`
* **Daftar (sequence)**: `SequenceWidget` dengan fungsi tambah/hapus item
* **Tanggal/Waktu**: `DateInputWidget`, `DateTimeInputWidget`

---

## Jenis Validasi

### Validator Bawaan

* `Length(min, max)` → panjang string
* `Range(min, max)` → rentang angka
* `Email()` → format email
* `Regex(pattern)` → cocokkan pola regex
* `OneOf(choices)` / `NoneOf(choices)` → nilai harus (atau tidak boleh) termasuk dalam daftar

### Validator Kustom

```python
def custom_validator(node, value):
    if not value.startswith('prefix_'):
        raise colander.Invalid(node, "Value must start with 'prefix_'")
```

---

## Penanganan Error

```python
try:
    appstruct = form.validate(controls)
except deform.ValidationFailure as e:
    return {'form': e.render()}
```

Pesan error kustom juga bisa ditentukan langsung di `SchemaNode`, misalnya jika input terlalu pendek atau kosong.

---

## Fitur yang Diterapkan

1. **Formulir Kontak**

   * Input nama, email, pesan
   * Validasi sisi server
   * Pesan sukses dengan flash message

2. **Formulir Registrasi Pengguna**

   * Validasi password, umur, dan email
   * Berbagai tipe input (teks, password, select)
   * Tampilan dengan Bootstrap

3. **Formulir Urutan (Sequence)**

   * Tambah/hapus item dinamis
   * Validasi jumlah minimal/maksimal item

4. **Validasi Lengkap**

   * Validasi sisi klien dan server
   * Pesan error yang jelas

5. **Antarmuka Pengguna (UI)**

   * Responsif
   * Indikator kekuatan password
   * Tampilan sukses/gagal yang jelas

---

## Pertimbangan Keamanan

* Perlindungan **CSRF** bawaan Pyramid
* Validasi input dari Colander mencegah **injeksi kode**
* Field password disembunyikan
* Data flash disimpan aman di sesi

---

## Praktik Terbaik

* Gunakan deskripsi field yang jelas
* Selalu validasi di sisi server
* Tangani error dengan ramah pengguna
* Redirect setelah submit berhasil
* Gunakan placeholder dan pesan bantuan

---

## Fitur Lanjutan

* **Widget Kustom**: membuat komponen input baru sesuai kebutuhan
* **Validator Kustom**: misalnya cek username unik ke database
* **Pre-population**: isi form dengan data yang sudah ada
* **Upload File**: mendukung input file menggunakan `FileUploadWidget()`

---

## Pengujian Aplikasi

1. Jalankan aplikasi:

   ```bash
   cd 18_Forms_and_Validation_with_Deform
   pserve development.ini
   ```
2. Tes tiap form di browser:

   * `/contact` → form kontak
   * `/user` → form registrasi
   * `/sequence` → form sequence

Uji validasi email, password, dan pesan flash untuk memastikan semuanya berjalan.

---

## Pertimbangan Performa

* Form di-render di sisi server
* Cache file CSS/JS statis
* Gunakan pagination untuk form besar
* Hindari terlalu banyak item dalam sequence

---

## Kesimpulan

Tutorial ini menunjukkan cara membuat dan memvalidasi form kompleks menggunakan **Deform** dan **Colander** dalam aplikasi **Pyramid**.
Fitur-fitur utama yang ditunjukkan:

* Definisi form berbasis skema
* Validasi lengkap (server & klien)
* Koleksi widget yang kaya
* Tampilan profesional dengan Bootstrap
* Keamanan dan UX yang baik

**Deform** menyediakan sistem form yang kuat, fleksibel, dan mudah diperluas—ideal untuk aplikasi Pyramid yang membutuhkan form dengan validasi canggih dan tampilan modern.
