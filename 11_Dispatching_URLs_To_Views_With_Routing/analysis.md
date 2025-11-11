# Tutorial 11: Dispatching URLs Ke Views Dengan Routing

## Gambaran Umum
Tutorial ini memperkenalkan sistem URL routing Pyramid, yang memetakan URLs ke fungsi view. Routing memungkinkan URLs yang bersih dan bermakna serta memisahkan struktur URL dari logic view.

## Konsep Kunci

### Konfigurasi Route
Routes memetakan pola URL ke named routes yang dapat direferensikan dalam views.

### Parameter URL
Mengekstrak nilai dinamis dari URLs menggunakan pola route.

### HTTP Exceptions
Menggunakan kelas exception Pyramid untuk redirects dan error responses.

## Detail Implementasi

### Definisi Route
```python
config.add_route('home', '/')
config.add_route('hello', '/howdy/{name}')
config.add_route('redirect', '/goto')
config.add_route('gone', '/gone')
```

### Ekstraksi Parameter
```python
@view_config(route_name='hello')
def hello(request):
    name = request.matchdict['name']
    return Response(f'Hello {name}!')
```

### HTTP Exceptions
```python
from pyramid.httpexceptions import HTTPFound, HTTPGone

@view_config(route_name='redirect')
def redirect(request):
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='gone')
def gone(request):
    return HTTPGone()
```

## Pola Route

### Static Routes
Routes sederhana yang mencocokkan URLs yang exact.

### Dynamic Routes
Routes dengan placeholder untuk bagian yang variabel.

### Parameter Opsional
Routes dengan segmen path opsional.

### Regular Expression Routes
Pattern matching lanjutan dengan regex.

## Generasi URL

### Route URLs
Menghasilkan URLs dari nama route dan parameter.

### Reverse Routing
Membuat URLs secara programmatic alih-alih hardcoding.

### Pembangunan URL
Membangun URLs dengan query parameters dan fragments.

## Pencocokan Route

### Pattern Matching
Bagaimana Pyramid mencocokkan URLs ke routes.

### Precedence
Urutan evaluasi route.

### Fallback Routes
Routes default untuk URLs yang tidak cocok.

## HTTP Exceptions

### Redirects
HTTPFound untuk temporary redirects.

### Permanent Redirects
HTTPMovedPermanently untuk permanent moves.

### Error Responses
HTTPNotFound, HTTPForbidden, dll.

### Custom Exceptions
Membuat exception khusus aplikasi.

## Routing Lanjutan

### Route Predicates
Memfilter routes berdasarkan kondisi.

### Custom Route Factories
Konfigurasi route lanjutan.

### Subdomain Routing
Routing berdasarkan subdomain.

### Internationalization
URL routing yang dilokalkan.

## Analisis

### Routing vs Traversal
Pendekatan URL dispatch vs object traversal.

### RESTful URLs
Mendesain struktur URL yang bersih dan bermakna.

### Pertimbangan SEO
Dampak struktur URL pada search engine optimization.

### Implikasi Keamanan
Menghindari serangan berbasis URL melalui routing yang proper.

### Performa
Efisiensi pencocokan route dan caching.

## Best Practices

### Desain URL
- Gunakan URLs yang deskriptif dan hierarkis
- Buat URLs pendek dan mudah diingat
- Gunakan lowercase dengan hyphens untuk readability
- Hindari query parameters jika memungkinkan

### Organisasi Route
- Kelompokkan routes terkait secara logis
- Gunakan konvensi penamaan yang konsisten
- Dokumentasikan tujuan route
- Rencanakan untuk perubahan URL di masa depan

### Error Handling
- Gunakan kode status HTTP yang tepat
- Berikan pesan error yang bermakna
- Tangani edge cases dengan baik
- Log errors untuk debugging

### Testing
- Test semua variasi route
- Verifikasi ekstraksi parameter
- Periksa kondisi error
- Validasi generasi URL

## Kesimpulan
URL routing adalah aspek fundamental dari pengembangan aplikasi web. Sistem routing Pyramid menyediakan tools yang powerful untuk membuat struktur URL yang bersih dan maintainable yang meningkatkan user experience dan arsitektur aplikasi. Memahami pola routing dan HTTP exceptions memungkinkan developer membangun aplikasi web yang robust dengan penanganan URL dan error management yang proper.