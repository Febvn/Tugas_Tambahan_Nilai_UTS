# Tutorial 10: Menangani Web Requests dan Responses

## Gambaran Umum
Tutorial ini mendemonstrasikan cara menangani HTTP requests dan membuat custom responses dalam aplikasi Pyramid. Tutorial ini mencakup objek Request dan Response, HTTP methods, dan kustomisasi response.

## Konsep Kunci

### Objek Request
Objek request berisi semua informasi tentang HTTP request yang masuk.

### Objek Response
Objek Response Pyramid memungkinkan kontrol penuh atas HTTP responses.

## Detail Implementasi

### Pembuatan Response Dasar
```python
from pyramid.response import Response

@view_config(route_name='home', request_method='GET')
def home(request):
    return Response('Home View')
```

### Penanganan HTTP Method
Fungsi view berbeda untuk HTTP methods berbeda pada route yang sama.

### Kustomisasi Response
- Header Content-Type
- Kode status
- Header kustom
- Body response

## Fitur Objek Request

### Mengakses Data Request
- `request.method`: HTTP method (GET, POST, dll.)
- `request.url`: URL lengkap
- `request.path`: Path URL
- `request.params`: Query parameters dan POST data
- `request.headers`: HTTP headers
- `request.cookies`: Data cookie

### Pemrosesan Request
- Ekstraksi parameter
- Inspeksi header
- Content negotiation
- Data autentikasi

## Fitur Objek Response

### Pembuatan Response
```python
response = Response('Hello World')
response.status_int = 200
response.content_type = 'text/plain'
```

### Jenis Response
- Text responses
- JSON responses
- File responses
- Redirect responses
- Error responses

### Header Response
- Content-Type
- Cache-Control
- Header kustom
- Cookies

## HTTP Methods

### GET Requests
Mengambil data dari server.

### POST Requests
Mengirimkan data untuk diproses.

### PUT Requests
Memperbarui resource yang ada.

### DELETE Requests
Menghapus resources.

## Content Types

### Text/HTML
Response text dan HTML dasar.

### JSON
Response data terstruktur.

### XML
Response markup language.

### Binary
Download file dan data binary.

## Error Handling

### Kode Status HTTP
- 200 OK
- 404 Not Found
- 500 Internal Server Error
- Kode status kustom

### Exception Views
Menangani exception dengan custom responses.

## Analisis

### Siklus Request-Response
1. Client mengirim HTTP request
2. Pyramid mencocokkan route dan view
3. Fungsi view menerima objek request
4. View memproses request dan membuat response
5. Response dikirim kembali ke client

### Best Practices
1. **Gunakan HTTP methods yang tepat**: GET untuk retrieval, POST untuk creation
2. **Set content types yang benar**: text/html, application/json, dll.
3. **Tangani error dengan baik**: Kembalikan kode status dan pesan yang proper
4. **Validasi input**: Periksa parameter dan data request
5. **Pertimbangan keamanan**: Sanitasi input, cegah XSS

### Pola Umum
1. **RESTful APIs**: Method berbeda untuk operasi CRUD
2. **Form handling**: GET untuk display, POST untuk submission
3. **AJAX endpoints**: JSON responses untuk JavaScript clients
4. **File serving**: Binary responses untuk downloads

### Pertimbangan Performa
- Minimalkan ukuran response
- Gunakan caching headers yang tepat
- Kompresi responses jika memungkinkan
- Stream responses yang besar

### Testing Request/Response Handling
- Test HTTP methods berbeda
- Verifikasi konten dan headers response
- Periksa kondisi error
- Validasi penanganan input

## Kesimpulan
Memahami penanganan request dan response adalah fundamental untuk web development dengan Pyramid. Framework ini menyediakan tools yang powerful untuk memproses incoming requests dan membuat responses yang tepat, memungkinkan developer membangun aplikasi web yang robust dan fleksibel yang menangani protokol HTTP dengan proper.