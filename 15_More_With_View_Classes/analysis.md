
---

# **Tutorial 15: Lebih Lanjut dengan View Class**

## **Ikhtisar**

Tutorial ini membahas pola dan teknik lanjutan dalam penggunaan *view class* di aplikasi Pyramid. Melanjutkan dari *view class* dasar yang dijelaskan pada tutorial 9, bagian ini menunjukkan penggunaan tingkat lanjut seperti penanganan banyak metode HTTP, berbagai *renderer*, *custom predicates*, dan desain API yang bersifat RESTful.

---

## **Konsep Utama**

### **Pola View Class Lanjutan**

Memahami konfigurasi kompleks dan *inheritance* pada *view class*.

### **Beberapa Metode HTTP**

Menangani berbagai *HTTP verb* dalam satu *view class*.

### **Custom Predicates**

Pencocokan *view* bersyarat berdasarkan karakteristik permintaan (*request*).

### **Desain Resource RESTful**

Menerapkan operasi CRUD menggunakan *view class*.

### **Manajemen Konteks Request**

Penanganan permintaan lanjutan dan pengoperan konteks antar komponen.

---

## **Detail Implementasi**

### **Pewarisan dan Default pada View Class**

```python
@view_defaults(route_name='company')
class CompanyViews:
    def __init__(self, request):
        self.request = request
        self.company_name = request.matchdict.get('name', '').lower()
```

Dekorator `@view_defaults` memungkinkan pengaturan konfigurasi umum yang berlaku untuk semua metode dalam *view class*. Ini mengurangi duplikasi kode dan memberikan cara yang rapi untuk berbagi logika inisialisasi.

---

### **Penanganan Banyak Metode HTTP**

```python
@view_config(request_method='GET', renderer='templates/company.html')
def company(self):
    # Penanganan GET

@view_config(request_method='PUT', renderer='json')
def update_company(self):
    # Penanganan PUT

@view_config(request_method='DELETE', renderer='json')
def delete_company(self):
    # Penanganan DELETE
```

Setiap metode dalam *view class* bisa diberi dekorator `@view_config` untuk menangani metode HTTP tertentu, memungkinkan satu kelas mengimplementasikan seluruh operasi CRUD untuk satu *resource*.

---

### **Custom Predicates**

```python
@view_config(route_name='home', request_method='GET',
             custom_predicates=[lambda info, request: request.params.get('debug') == 'true'],
             renderer='templates/debug.html')
def debug_info(self):
    # Hanya dipanggil jika ?debug=true
```

*Custom predicate* memungkinkan pencocokan *view* berdasarkan karakteristik permintaan tertentu, membuat logika *routing* menjadi lebih fleksibel.

---

### **Endpoint API JSON**

```python
@view_config(route_name='company_json', request_method='GET', renderer='json')
def company_json(self):
    return {
        'company': self.company_data,
        'api_version': '1.0'
    }
```

*Renderer JSON* secara otomatis mengubah objek Python menjadi respons JSON, membuat pengembangan API menjadi lebih sederhana.

---

## **Pola View Class**

### **View Berbasis Resource**

Mengorganisir *view* berdasarkan sumber daya yang memiliki beberapa operasi:

```python
@view_defaults(route_name='resource')
class ResourceViews:
    def __init__(self, request):
        self.request = request
        self.resource_id = request.matchdict.get('id')

    @view_config(request_method='GET')
    def get(self): pass

    @view_config(request_method='POST')
    def create(self): pass

    @view_config(request_method='PUT')
    def update(self): pass

    @view_config(request_method='DELETE')
    def delete(self): pass
```

---

### **View yang Kontekstual**

*View* yang menyesuaikan perilaku berdasarkan konteks *request*:

```python
class ContextViews:
    def __init__(self, request):
        self.request = request
        self.is_api = request.accept.contains('application/json')

    @view_config(renderer='json' if self.is_api else 'templates/page.html')
    def index(self):
        return self.get_data()
```

---

### **View Class Bertingkat**

Menggunakan *inheritance* untuk fungsi umum:

```python
class BaseViews:
    def __init__(self, request):
        self.request = request

    def check_permissions(self):
        # Pemeriksaan izin umum

class AdminViews(BaseViews):
    @view_config(route_name='admin')
    def admin_panel(self):
        self.check_permissions()
        # Logika khusus admin
```

---

## **Penanganan Metode HTTP**

### **GET (Mengambil Data)**

```python
@view_config(request_method='GET')
def retrieve_data(self):
    data = self.get_data_from_database()
    return {'data': data}
```

### **POST (Membuat Data Baru)**

```python
@view_config(request_method='POST', renderer='json')
def create_resource(self):
    data = self.request.json_body
    new_resource = self.create_in_database(data)
    return {'id': new_resource.id, 'status': 'created'}
```

### **PUT (Memperbarui Data)**

```python
@view_config(request_method='PUT', renderer='json')
def update_resource(self):
    data = self.request.json_body
    resource_id = self.request.matchdict['id']
    updated = self.update_in_database(resource_id, data)
    return {'status': 'updated', 'resource': updated}
```

### **DELETE (Menghapus Data)**

```python
@view_config(request_method='DELETE', renderer='json')
def delete_resource(self):
    resource_id = self.request.matchdict['id']
    self.delete_from_database(resource_id)
    return {'status': 'deleted'}
```

---

## **Custom Predicates**

### **Berdasarkan Query Parameter**

```python
def debug_mode_predicate(info, request):
    return request.params.get('debug') == 'true'

@view_config(custom_predicates=[debug_mode_predicate])
def debug_view(self): pass
```

### **Berdasarkan Header**

```python
def api_version_predicate(info, request):
    version = request.headers.get('X-API-Version', '1.0')
    return version == '2.0'

@view_config(custom_predicates=[api_version_predicate])
def v2_api_view(self): pass
```

### **Berdasarkan User Agent**

```python
def mobile_predicate(info, request):
    ua = request.headers.get('User-Agent', '').lower()
    return 'mobile' in ua or 'android' in ua

@view_config(custom_predicates=[mobile_predicate])
def mobile_view(self): pass
```

---

## **Penanganan Error**

### **Kode Status HTTP**

```python
@view_config(request_method='GET')
def get_resource(self):
    resource = self.find_resource()
    if not resource:
        response = Response('Not Found', status=404)
        return response
    return {'resource': resource}
```

### **Respons JSON Error**

```python
@view_config(request_method='POST', renderer='json')
def create_resource(self):
    try:
        data = self.request.json_body
        resource = self.create_resource(data)
        return {'status': 'success', 'resource': resource}
    except ValidationError as e:
        return {'error': 'validation_failed', 'details': str(e)}
    except Exception as e:
        return {'error': 'internal_error', 'message': str(e)}
```

---

## **Pemrosesan Request**

### **Parsing JSON**

```python
@view_config(request_method='POST', renderer='json')
def process_json(self):
    try:
        data = self.request.json_body
        # Proses data
        return {'result': 'processed'}
    except ValueError:
        return {'error': 'Invalid JSON'}
```

### **Menangani Form Data**

```python
@view_config(request_method='POST')
def process_form(self):
    data = dict(self.request.POST)
    # Proses form
    return {'received': data}
```

### **Upload File**

```python
@view_config(request_method='POST')
def upload_file(self):
    file = self.request.POST['file']
    # Proses file upload
    filename = self.save_file(file)
    return {'filename': filename, 'status': 'uploaded'}
```

---

## **Konfigurasi Lanjutan**

### **Pewarisan Konfigurasi View**

```python
@view_defaults(renderer='json', permission='view')
class APIViews:
    pass

class UserAPIViews(APIViews):
    @view_config(route_name='users')
    def users(self): pass

    @view_config(route_name='user', permission='edit')  # Ganti izin
    def user(self): pass
```

### **Context Factory**

```python
def user_context_factory(request):
    user_id = request.matchdict['user_id']
    user = get_user(user_id)
    if not user:
        raise HTTPNotFound()
    return user

@view_config(route_name='user', context=user_context_factory)
def user_view(request):
    user = request.context  # Objek user
    return {'user': user}
```

---

## **Pengujian View Class**

### **Unit Test**

```python
def test_company_view():
    request = testing.DummyRequest()
    request.matchdict = {'name': 'acme'}
    view = CompanyViews(request)
    response = view.company()
    assert 'company' in response
```

### **Integration Test**

```python
def test_company_api(app):
    response = app.get('/company/acme/json')
    assert response.status_code == 200
    data = response.json
    assert 'company' in data
```

### **Functional Test**

```python
def test_company_crud(app):
    # Create
    response = app.post_json('/company', {'name': 'test'})
    assert response.status_code == 201

    # Read
    response = app.get('/company/test')
    assert response.status_code == 200

    # Update
    response = app.put_json('/company/test', {'name': 'updated'})
    assert response.status_code == 200

    # Delete
    response = app.delete('/company/test')
    assert response.status_code == 204
```

---

## **Pertimbangan Performa**

* **Inisialisasi View Class**: Setiap permintaan membuat instance baru, jadi `__init__` harus ringan.
* **Caching**: Gunakan cache untuk operasi berat.

```python
@view_config(request_method='GET')
def cached_view(self):
    @cache_region('default', 'company_data')
    def get_company_data(company_id):
        return self.query_database(company_id)

    return get_company_data(self.company_id)
```

* **Optimasi Database**: Gunakan query efisien dan pagination untuk data besar.

---

## **Keamanan**

### **Validasi Input**

```python
@view_config(request_method='POST', renderer='json')
def create_user(self):
    schema = UserSchema()
    try:
        data = schema.deserialize(self.request.json_body)
        user = self.create_user(data)
        return {'user': user}
    except ValidationError as e:
        return {'error': 'validation_failed', 'details': e.messages}
```

### **Pemeriksaan Izin**

```python
@view_config(request_method='DELETE', permission='delete')
def delete_resource(self):
    # Pyramid otomatis cek izin
    self.delete_resource()
    return {'status': 'deleted'}
```

### **Perlindungan CSRF**

```python
@view_config(request_method='POST', require_csrf=True)
def update_resource(self):
    data = self.request.json_body
    return self.update_resource(data)
```

---

## **Pola Dunia Nyata**

### **Versi API**

```python
@view_defaults(route_name='api')
class APIv1Views:
    api_version = '1.0'

@view_defaults(route_name='api', custom_predicates=[version_predicate('2.0')])
class APIv2Views:
    api_version = '2.0'
```

### **Negosiasi Konten**

```python
class ContentViews:
    @view_config(request_method='GET', accept='application/json', renderer='json')
    def json_view(self): pass

    @view_config(request_method='GET', accept='text/html', renderer='templates/page.html')
    def html_view(self): pass
```

### **Pagination**

```python
@view_config(request_method='GET', renderer='json')
def list_resources(self):
    page = int(self.request.params.get('page', 1))
    per_page = int(self.request.params.get('per_page', 20))

    resources, total = self.get_paginated_resources(page, per_page)

    return {
        'resources': resources,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }
    }
```

---

## **Analisis**

### **Keuntungan View Class Lanjutan**

* **Organisasi kode**: fungsi terkait dikelompokkan dengan rapi
* **DRY principle**: menghindari duplikasi dengan pewarisan
* **Fleksibilitas**: dukungan multi-renderer & multi-method
* **Mudah dirawat**: logika terstruktur
* **Mudah diuji**: tiap metode bisa diuji terpisah

### **Dampak Performa**

* Setiap *view class* dibuat ulang per request
* Gunakan cache untuk operasi berat
* Optimalkan penggunaan memori

### **Faktor Skalabilitas**

* Optimasi query database
* Gunakan caching layer
* Desain stateless untuk load balancing

### **Best Practice**

* Satu *view class* = satu jenis resource
* Pisahkan logika bisnis ke service lain
* Gunakan pola REST yang konsisten
* Tangani error dengan rapi
* Dokumentasi API yang jelas

---

## **Kesimpulan**

*View class* tingkat lanjut memberikan pola yang kuat untuk membangun aplikasi web yang kompleks. Dengan memanfaatkan banyak metode HTTP, *custom predicates*, dan konfigurasi yang fleksibel, pengembang bisa membuat aplikasi Pyramid yang mudah dikelola, skalabel, dan kaya fitur. Pemahaman konsep ini membantu menciptakan kode profesional yang bersih dan terorganisir sesuai praktik terbaik pengembangan web.

---


