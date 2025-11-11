# Tutorial 12: Templating With jinja2

## Overview
This tutorial introduces Jinja2 templating in Pyramid applications, demonstrating how to separate presentation logic from application logic using powerful template rendering.

## Key Concepts

### Template Engines
Jinja2 as a modern, fast template engine for Python.

### Template Rendering
How Pyramid integrates with Jinja2 for HTML generation.

### Template Variables
Passing data from views to templates.

## Implementation Details

### Configuration
```python
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
```

### View Configuration
```python
@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return {'name': 'Home View'}
```

### Template Syntax
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

## Template Features

### Variable Interpolation
Inserting Python variables into templates.

### Control Structures
- `{% if %}` conditions
- `{% for %}` loops
- `{% set %}` variable assignment

### Filters
Transforming variables in templates.

### Template Inheritance
Base templates and extending them.

## Jinja2 vs Chameleon

### Syntax Comparison
- Jinja2: `{{ variable }}`, `{% if %}`
- Chameleon: `${variable}`, `tal:condition`

### Performance
Both are fast, but Jinja2 is generally faster for complex templates.

### Features
Jinja2 has more built-in filters and functions.

### Ecosystem
Jinja2 is widely used outside Pyramid.

## Advanced Templating

### Macros
Reusable template components.

### Includes
Including other templates.

### Custom Filters
Creating application-specific filters.

### Template Context
Managing template variables and scope.

## Template Organization

### Directory Structure
Organizing templates in logical directories.

### Naming Conventions
Consistent template naming.

### Asset Management
Handling CSS, JavaScript, and images.

### Template Caching
Performance optimization for templates.

## Analysis

### Separation of Concerns
Benefits of separating logic from presentation.

### Maintainability
Easier maintenance with template separation.

### Reusability
Template reuse across different views.

### Performance Considerations
Template compilation and caching.

### Security
Preventing template injection attacks.

## Best Practices

### Template Structure
- Use consistent directory structure
- Keep templates small and focused
- Use meaningful variable names
- Document template purpose

### Variable Passing
- Pass only necessary data to templates
- Use dictionaries for complex data
- Avoid business logic in templates
- Sanitize user input

### Template Inheritance
- Create base templates for common elements
- Use blocks for customizable sections
- Keep inheritance hierarchy simple
- Document block purposes

### Performance
- Enable template caching in production
- Minimize template complexity
- Use appropriate filters
- Profile template rendering

### Security
- Escape user input automatically
- Use safe filters when needed
- Validate template data
- Avoid template injection

## Conclusion
Jinja2 templating provides a powerful and flexible way to generate HTML in Pyramid applications. Its clean syntax, extensive features, and performance make it an excellent choice for modern web development. Understanding template organization, variable passing, and best practices enables developers to create maintainable and efficient web applications.
