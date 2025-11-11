# Tutorial 08: HTML Generation With Templating

## Overview
This tutorial introduces HTML templating in Pyramid applications using Chameleon templates. Templates allow separation of presentation logic from application logic, enabling dynamic HTML generation with data passed from views.

## Key Concepts

### Templating in Pyramid
Templates are files that contain HTML with placeholders for dynamic content. Pyramid supports multiple templating engines, with Chameleon being the default.

### Chameleon Templates
Chameleon is a fast, secure templating engine that compiles templates to Python bytecode. It uses TAL (Template Attribute Language) for dynamic content insertion.

## Implementation Details

### Template Configuration
```python
config.add_static_view(name='static', path='tutorial:static')
```

### View Functions with Templates
```python
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'name': 'Home View'}

@view_config(route_name='hello', renderer='templates/hello.pt')
def hello(request):
    return {'name': 'Hello View'}
```

### Template Syntax
Chameleon templates use TAL attributes for dynamic content:

- `${variable}` - Variable substitution
- `tal:condition` - Conditional rendering
- `tal:repeat` - Looping over collections
- `tal:define` - Variable definition

## Template Structure

### HTML5 Boilerplate
Templates include proper HTML5 structure with:
- DOCTYPE declaration
- Meta tags for charset, viewport, description
- Favicon links
- Semantic HTML elements

### Static Asset Integration
Templates reference static files using `request.static_url()`:
```html
<img src="${request.static_url('tutorial:static/pyramid.png')}">
<link rel="shortcut icon" href="${request.static_url('tutorial:static/pyramid-16x16.png')}">
```

### URL Generation
Templates use `request.route_url()` for internal links:
```html
<a href="${request.route_url('hello')}">Hello World</a>
```

## Template Files

### home.pt
The home page template displays:
- Pyramid logo and branding
- Welcome message with dynamic name
- Navigation links to other pages

### hello.pt
The hello page template shows:
- Similar structure to home.pt
- Different welcome message
- Link back to home page

## Static Assets

### Images
- `pyramid.png` - Main Pyramid logo (150px height)
- `pyramid-16x16.png` - Favicon (16x16 pixels)

### Asset Serving
Static files are served through Pyramid's static view configuration, making them accessible via URLs like `/static/pyramid.png`.

## Analysis

### Advantages of Templating
1. **Separation of Concerns**: HTML markup separate from Python logic
2. **Maintainability**: Easier to modify presentation without touching code
3. **Reusability**: Templates can be shared across views
4. **Designer-Friendly**: HTML designers can work independently

### Chameleon vs Other Templating Engines
1. **Chameleon**: Fast compilation, secure, XML-compliant
2. **Jinja2**: More flexible syntax, better error messages
3. **Mako**: Python-like syntax, good performance

### Template Best Practices
1. **Semantic HTML**: Use proper HTML5 elements
2. **Accessibility**: Include alt text, proper headings
3. **Performance**: Minimize template complexity
4. **Organization**: Group related templates in subdirectories

### Template Inheritance
While not demonstrated here, Chameleon supports:
- Template inheritance with METAL
- Macro definitions and usage
- Slot filling for flexible layouts

### Static Asset Management
1. **Versioning**: Cache-busting with versioned URLs
2. **CDN Integration**: External hosting for performance
3. **Minification**: Compressed CSS/JS for production
4. **Organization**: Logical directory structure

## Conclusion
Templating is essential for modern web applications, providing clean separation between presentation and logic. Chameleon's TAL syntax offers powerful yet secure template capabilities, making it an excellent choice for Pyramid applications. The combination of dynamic templates and static asset serving enables rich, interactive web experiences.
