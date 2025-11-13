# Tutorial 14: Pengembangan AJAX dengan JSON Renderer

## Gambaran Umum

Tutorial ini menjelaskan cara mengimplementasikan fungsionalitas **AJAX (Asynchronous JavaScript and XML)** di aplikasi **Pyramid** dengan menggunakan **JSON renderer**. Walaupun namanya menyebut XML, praktik modern AJAX biasanya menggunakan **JSON** sebagai format pertukaran data antara klien dan server.

---

## Konsep Utama

### Dasar AJAX

Memahami cara kerja permintaan web secara **asinkron (tidak menunggu)**.

### JSON Renderer

Kemampuan bawaan Pyramid untuk menghasilkan output dalam format JSON.

### Desain API RESTful

Prinsip-prinsip dasar dalam merancang API web.

### Komunikasi Klien-Server

Cara browser berkomunikasi dengan server secara asinkron.

---

## Detail Implementasi

### Konfigurasi JSON Renderer

```python
@view_config(route_name='api_data', renderer='json')
def api_data(request):
    return {'message': 'Hello', 'data': [1, 2, 3]}
```

### Penanganan Permintaan AJAX

```javascript
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data));
```

### Penanganan Metode Request

```python
@view_config(route_name='api_echo', renderer='json', request_method='POST')
def api_echo(request):
    data = request.json_body
    return {'echo': data}
```

---

## Konsep AJAX

### Komunikasi Asinkron

* Permintaan non-blocking
* Pengalaman pengguna yang lebih baik
* Pembaruan data secara real-time
* Peningkatan performa UI

### XMLHttpRequest vs Fetch API

* **XMLHttpRequest:** API lama
* **Fetch API:** Modern, berbasis Promise
* **Pertimbangan kompatibilitas browser**
* **Perbedaan dalam penanganan error**

### Format Data JSON

* Format pertukaran data yang ringan
* Independen dari bahasa pemrograman
* Mudah dibaca manusia
* Mudah di-parse dan dibangkitkan

---

## Fitur JSON Renderer

### Serialisasi Otomatis

```python
# Objek Python otomatis dikonversi ke JSON
return {
    'datetime': datetime.now(),
    'data': [1, 2, 3],
    'nested': {'key': 'value'}
}
```

### Serialisasi Kustom

```python
import json
from pyramid.renderers import JSON

json_renderer = JSON()
json_renderer.add_adapter(MyClass, lambda obj, request: obj.to_dict())
```

### Header Content-Type

* Otomatis menambahkan header `application/json`
* Menangani kode status HTTP dengan benar
* Dukungan CORS (Cross-Origin Resource Sharing)

---

## Pola Desain API

### Endpoint RESTful

* URL berbasis resource
* Menggunakan metode HTTP sesuai fungsi
* Operasi stateless
* Mengikuti standar kode status HTTP

### Pola Request/Response

* Struktur data konsisten
* Format penanganan error
* Dukungan pagination
* Filtering dan sorting

### Strategi Versi API

* Versi lewat URL: `/api/v1/data`
* Versi lewat header: `Accept: application/vnd.api.v1+json`
* Negosiasi konten otomatis

---

## AJAX di Sisi Klien

### Penggunaan Fetch API

```javascript
// Permintaan GET
fetch('/api/data')
    .then(response => response.json())
    .then(data => updateUI(data));

// Permintaan POST
fetch('/api/echo', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: 'John'})
})
.then(response => response.json())
.then(data => console.log(data));
```

### Penanganan Error

```javascript
fetch('/api/data')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    })
    .catch(error => handleError(error));
```

### Status Loading

```javascript
function showLoading() {
    button.disabled = true;
    button.textContent = 'Loading...';
}

function hideLoading() {
    button.disabled = false;
    button.textContent = 'Submit';
}
```

---

## Pemrosesan Request

### Parsing Body JSON

```python
@view_config(renderer='json', request_method='POST')
def process_data(request):
    try:
        data = request.json_body
        # Proses data
        return {'status': 'success', 'processed': data}
    except ValueError:
        return {'status': 'error', 'message': 'Invalid JSON'}
```

### Penanganan Form Data

```python
@view_config(renderer='json', request_method='POST')
def process_form(request):
    data = dict(request.POST)
    return {'received': data}
```

### Penanganan Upload File

```python
@view_config(renderer='json', request_method='POST')
def upload_file(request):
    file = request.POST['file']
    # Proses file upload
    return {'status': 'uploaded', 'filename': file.filename}
```

---

## Pertimbangan Keamanan

### Perlindungan CSRF

* Menggunakan token
* Kebijakan same-origin
* Konfigurasi CORS yang aman

### Validasi Input

* Validasi dengan JSON Schema
* Sanitasi data
* Pengecekan tipe

### Pembatasan Akses

* Rate limiting
* Kuota API
* Pencegahan penyalahgunaan

---

## Optimasi Performa

### Strategi Caching

* Header caching HTTP
* Dukungan ETag
* Conditional request

### Kompresi

* Kompresi GZIP
* Optimasi ukuran respon
* Minimalkan payload

### Manajemen Koneksi

* Gunakan keep-alive
* Pooling koneksi
* Penanganan timeout

---

## Penanganan Error

### Kode Status HTTP

* **200:** Berhasil
* **400:** Permintaan Salah
* **401:** Tidak Terotorisasi
* **404:** Tidak Ditemukan
* **500:** Kesalahan Server

### Format Respon Error

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {"field": "email", "issue": "invalid format"}
    }
}
```

### Penanganan Error di Klien

```javascript
function handleApiError(error) {
    if (error.status === 400) {
        showValidationErrors(error.details);
    } else if (error.status === 401) {
        redirectToLogin();
    } else {
        showGenericError(error.message);
    }
}
```

---

## Pengujian Aplikasi AJAX

### Unit Test View

```python
def test_api_data_view():
    request = testing.DummyRequest()
    response = api_data(request)
    assert response['status'] == 'success'
```

### Functional Testing

```python
def test_api_endpoint(app):
    response = app.get('/api/data')
    assert response.status_code == 200
    data = response.json
    assert 'message' in data
```

### Integration Testing

```python
def test_ajax_workflow(app):
    # Menguji seluruh alur kerja AJAX
    response = app.post_json('/api/echo', {'test': 'data'})
    assert response.status_code == 200
```

---

## Kompatibilitas Browser

### Dukungan Fetch API

* Browser modern: Didukung penuh
* IE11: Butuh polyfill
* Browser mobile: Umumnya didukung

### Pertimbangan CORS

* Kebijakan same-origin
* Preflight request
* Penanganan kredensial

---

## Pola di Dunia Nyata

### Pagination

```json
{
    "data": [...],
    "pagination": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "total_pages": 5
    }
}
```

### Filtering dan Sorting

```javascript
const params = new URLSearchParams({
    filter: 'active',
    sort: 'name',
    page: 1
});
fetch(`/api/users?${params}`)
```

### Pembaruan Data Real-time

* WebSocket untuk data real-time
* Server-Sent Events (SSE)
* Long polling sebagai fallback

---

## Analisis

### Keuntungan AJAX

* UX lebih cepat dan responsif
* Mengurangi beban server
* Mendukung progressive enhancement
* Membuka jalan ke Single Page Application (SPA)

### Pertimbangan Performa

* Perbandingan antara load awal dan dynamic loading
* Strategi caching yang efektif
* Dampak ukuran bundle

### Implikasi Keamanan

* Pencegahan XSS
* Proteksi CSRF
* Validasi input
* Penanganan autentikasi

### Faktor Skalabilitas

* Pembatasan kuota API
* Lapisan caching
* Optimasi database
* Integrasi CDN

---

## Kesimpulan

AJAX dengan JSON Renderer di Pyramid memungkinkan komunikasi cepat dan dinamis antara klien dan server tanpa perlu memuat ulang halaman. Dengan desain RESTful, validasi input yang aman, serta penerapan strategi performa dan keamanan, aplikasi web menjadi lebih **interaktif, efisien, dan scalable**.
