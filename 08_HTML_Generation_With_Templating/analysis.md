# Tutorial 08: Generasi HTML Dengan Templating

## Gambaran Umum
Tutorial ini memperkenalkan HTML templating dalam aplikasi Pyramid menggunakan Chameleon templates. Templates memungkinkan pemisahan presentation logic dari application logic, memungkinkan generasi HTML dinamis dengan data yang dikirim dari views.

## Konsep Kunci

### Templating dalam Pyramid
Templates adalah file yang berisi HTML dengan placeholder untuk konten dinamis. Pyramid mendukung multiple templating engines, dengan Chameleon sebagai default.

### Chameleon Templates
Chameleon adalah templating engine yang cepat dan aman yang mengkompilasi templates ke Python bytecode. Menggunakan TAL (Template Attribute Language) untuk penyisipan konten dinamis.

## Detail Implementasi

### Konfigurasi Template
```python
config.add_static_view(name='static', path='tutorial:static')
```

### Fungsi View dengan Templates
```python
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'name': 'Home View'}

@view_config(route_name='hello', renderer='templates/hello.pt')
def hello(request):
    return {'name': 'Hello View'}
```

### Sintaks Template
Chameleon templates menggunakan atribut TAL untuk konten dinamis:

- `${variable}` - Substitusi variabel
- `tal:condition` - Rendering kondisional
- `tal:repeat` - Looping atas koleksi
- `tal:define` - Definisi variabel

## Struktur Template

### HTML5 Boilerplate
Templates mencakup struktur HTML5 yang proper dengan:
- Deklarasi DOCTYPE
- Meta tags untuk charset, viewport, description
- Link favicon
- Elemen HTML semantik

### Integrasi Static Asset
Templates mereferensi file statis menggunakan `request.static_url()`:
```html
<img src="${request.static_url('tutorial:static/pyramid.png')}">
<link rel="shortcut icon" href="${request.static_url('tutorial:static/pyramid-16x16.png')}">
```

### Generasi URL
Templates menggunakan `request.route_url()` untuk link internal:
```html
<a href="${request.route_url('hello')}">Hello World</a>
```

## File Template

### home.pt
Template halaman home menampilkan:
- Logo dan branding Pyramid
- Pesan welcome dengan nama dinamis
- Link navigasi ke halaman lain

### hello.pt
Template halaman hello menampilkan:
- Struktur serupa dengan home.pt
- Pesan welcome yang berbeda
- Link kembali ke halaman home

## Static Assets

### Images
- `pyramid.png` - Logo Pyramid utama (tinggi 150px)
- `pyramid-16x16.png` - Favicon (16x16 pixels)

### Penyajian Asset
File statis disajikan melalui konfigurasi static view Pyramid, membuatnya dapat diakses melalui URLs seperti `/static/pyramid.png`.

## Analisis

### Keuntungan Templating
1. **Separation of Concerns**: Markup HTML terpisah dari logic Python
2. **Maintainability**: Lebih mudah memodifikasi presentation tanpa menyentuh kode
3. **Reusability**: Templates dapat dibagikan antar views
4. **Designer-Friendly**: Designer HTML dapat bekerja secara independen

### Chameleon vs Templating Engines Lain
1. **Chameleon**: Kompilasi cepat, aman, XML-compliant
2. **Jinja2**: Sintaks lebih fleksibel, pesan error lebih baik
3. **Mako**: Sintaks seperti Python, performa bagus

### Best Practices Template
1. **Semantic HTML**: Gunakan elemen HTML5 yang proper
2. **Accessibility**: Sertakan alt text, heading yang proper
3. **Performance**: Minimalkan kompleksitas template
4. **Organization**: Kelompokkan templates terkait dalam subdirektori

### Template Inheritance
Meskipun tidak didemonstrasikan di sini, Chameleon mendukung:
- Template inheritance dengan METAL
- Definisi dan penggunaan macro
- Slot filling untuk layout yang fleksibel

### Manajemen Static Asset
1. **Versioning**: Cache-busting dengan versioned URLs
2. **CDN Integration**: External hosting untuk performa
3. **Minification**: CSS/JS terkompresi untuk production
4. **Organization**: Struktur direktori yang logis

## Kesimpulan
Templating sangat penting untuk aplikasi web modern, menyediakan pemisahan yang bersih antara presentation dan logic. Sintaks TAL Chameleon menawarkan kemampuan template yang powerful namun aman, menjadikannya pilihan excellent untuk aplikasi Pyramid. Kombinasi template dinamis dan penyajian static asset memungkinkan pengalaman web yang kaya dan interaktif.