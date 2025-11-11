# Tutorial 15: More With View Classes

## Overview
This tutorial explores advanced patterns and techniques for using view classes in Pyramid applications. Building on the basic view classes introduced in tutorial 9, this tutorial demonstrates sophisticated view class usage including multiple HTTP methods, different renderers, custom predicates, and RESTful API design.

## Key Concepts

### Advanced View Class Patterns
Understanding complex view class configurations and inheritance.

### Multiple HTTP Methods
Handling different HTTP verbs within a single view class.

### Custom Predicates
Conditional view matching based on request characteristics.

### RESTful Resource Design
Implementing CRUD operations with view classes.

### Request Context Management
Advanced request handling and context passing.

## Implementation Details

### View Class Inheritance and Defaults

```python
@view_defaults(route_name='company')
class CompanyViews:
    def __init__(self, request):
        self.request = request
        self.company_name = request.matchdict.get('name', '').lower()
```

The `@view_defaults` decorator allows setting common configuration that applies to all methods in the view class. This reduces code duplication and provides a clean way to share setup logic.

### Multiple HTTP Method Handling

```python
@view_config(request_method='GET', renderer='templates/company.html')
def company(self):
    # GET request handling

@view_config(request_method='PUT', renderer='json')
def update_company(self):
    # PUT request handling

@view_config(request_method='DELETE', renderer='json')
def delete_company(self):
    # DELETE request handling
```

Each method in the view class can be decorated with `@view_config` to handle specific HTTP methods, allowing a single view class to implement full CRUD operations for a resource.

### Custom Predicates

```python
@view_config(route_name='home', request_method='GET',
             custom_predicates=[lambda info, request: request.params.get('debug') == 'true'],
             renderer='templates/debug.html')
def debug_info(self):
    # Only called when ?debug=true
```

Custom predicates allow conditional view matching based on arbitrary request characteristics, enabling sophisticated routing logic.

### JSON API Endpoints

```python
@view_config(route_name='company_json', request_method='GET', renderer='json')
def company_json(self):
    return {
        'company': self.company_data,
        'api_version': '1.0'
    }
```

JSON renderers automatically serialize Python objects to JSON responses, making API development straightforward.

## View Class Patterns

### Resource-Based Views
Organizing views around resources with multiple operations:

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

### Context-Aware Views
Views that adapt behavior based on request context:

```python
class ContextViews:
    def __init__(self, request):
        self.request = request
        self.is_api = request.accept.contains('application/json')

    @view_config(renderer='json' if self.is_api else 'templates/page.html')
    def index(self):
        return self.get_data()
```

### Hierarchical View Classes
Using inheritance for common functionality:

```python
class BaseViews:
    def __init__(self, request):
        self.request = request

    def check_permissions(self):
        # Common permission checking

class AdminViews(BaseViews):
    @view_config(route_name='admin')
    def admin_panel(self):
        self.check_permissions()
        # Admin-specific logic
```

## HTTP Method Handling

### GET Requests
Used for retrieving data:

```python
@view_config(request_method='GET')
def retrieve_data(self):
    data = self.get_data_from_database()
    return {'data': data}
```

### POST Requests
Used for creating new resources:

```python
@view_config(request_method='POST', renderer='json')
def create_resource(self):
    data = self.request.json_body
    new_resource = self.create_in_database(data)
    return {'id': new_resource.id, 'status': 'created'}
```

### PUT Requests
Used for updating existing resources:

```python
@view_config(request_method='PUT', renderer='json')
def update_resource(self):
    data = self.request.json_body
    resource_id = self.request.matchdict['id']
    updated = self.update_in_database(resource_id, data)
    return {'status': 'updated', 'resource': updated}
```

### DELETE Requests
Used for removing resources:

```python
@view_config(request_method='DELETE', renderer='json')
def delete_resource(self):
    resource_id = self.request.matchdict['id']
    self.delete_from_database(resource_id)
    return {'status': 'deleted'}
```

## Custom Predicates

### Query Parameter Predicates

```python
def debug_mode_predicate(info, request):
    return request.params.get('debug') == 'true'

@view_config(custom_predicates=[debug_mode_predicate])
def debug_view(self): pass
```

### Header-Based Predicates

```python
def api_version_predicate(info, request):
    version = request.headers.get('X-API-Version', '1.0')
    return version == '2.0'

@view_config(custom_predicates=[api_version_predicate])
def v2_api_view(self): pass
```

### User Agent Predicates

```python
def mobile_predicate(info, request):
    ua = request.headers.get('User-Agent', '').lower()
    return 'mobile' in ua or 'android' in ua

@view_config(custom_predicates=[mobile_predicate])
def mobile_view(self): pass
```

## Error Handling

### HTTP Status Codes

```python
@view_config(request_method='GET')
def get_resource(self):
    resource = self.find_resource()
    if not resource:
        response = Response('Not Found', status=404)
        return response
    return {'resource': resource}
```

### JSON Error Responses

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

## Request Processing

### JSON Body Parsing

```python
@view_config(request_method='POST', renderer='json')
def process_json(self):
    try:
        data = self.request.json_body
        # Process data
        return {'result': 'processed'}
    except ValueError:
        return {'error': 'Invalid JSON'}
```

### Form Data Handling

```python
@view_config(request_method='POST')
def process_form(self):
    data = dict(self.request.POST)
    # Process form data
    return {'received': data}
```

### File Upload Handling

```python
@view_config(request_method='POST')
def upload_file(self):
    file = self.request.POST['file']
    # Process uploaded file
    filename = self.save_file(file)
    return {'filename': filename, 'status': 'uploaded'}
```

## Advanced Configuration

### View Configuration Inheritance

```python
@view_defaults(renderer='json', permission='view')
class APIViews:
    pass

class UserAPIViews(APIViews):
    @view_config(route_name='users')
    def users(self): pass

    @view_config(route_name='user', permission='edit')  # Override permission
    def user(self): pass
```

### Context Factories

```python
def user_context_factory(request):
    user_id = request.matchdict['user_id']
    user = get_user(user_id)
    if not user:
        raise HTTPNotFound()
    return user

@view_config(route_name='user', context=user_context_factory)
def user_view(request):
    user = request.context  # User object
    return {'user': user}
```

## Testing View Classes

### Unit Testing

```python
def test_company_view():
    request = testing.DummyRequest()
    request.matchdict = {'name': 'acme'}
    view = CompanyViews(request)
    response = view.company()
    assert 'company' in response
```

### Integration Testing

```python
def test_company_api(app):
    response = app.get('/company/acme/json')
    assert response.status_code == 200
    data = response.json
    assert 'company' in data
```

### Functional Testing

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

## Performance Considerations

### View Class Instantiation
View classes are instantiated per request, so keep `__init__` methods lightweight.

### Caching Strategies
Use appropriate caching for expensive operations:

```python
@view_config(request_method='GET')
def cached_view(self):
    @cache_region('default', 'company_data')
    def get_company_data(company_id):
        return self.query_database(company_id)

    return get_company_data(self.company_id)
```

### Database Optimization
Use efficient queries and consider pagination for large datasets.

## Security Considerations

### Input Validation

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

### Permission Checking

```python
@view_config(request_method='DELETE', permission='delete')
def delete_resource(self):
    # Permission automatically checked by Pyramid
    self.delete_resource()
    return {'status': 'deleted'}
```

### CSRF Protection

```python
@view_config(request_method='POST', require_csrf=True)
def update_resource(self):
    # CSRF token automatically validated
    data = self.request.json_body
    return self.update_resource(data)
```

## Real-World Patterns

### API Versioning

```python
@view_defaults(route_name='api')
class APIv1Views:
    api_version = '1.0'

@view_defaults(route_name='api', custom_predicates=[version_predicate('2.0')])
class APIv2Views:
    api_version = '2.0'
```

### Content Negotiation

```python
class ContentViews:
    @view_config(request_method='GET', accept='application/json', renderer='json')
    def json_view(self): pass

    @view_config(request_method='GET', accept='text/html', renderer='templates/page.html')
    def html_view(self): pass
```

### Pagination Support

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

## Analysis

### Benefits of Advanced View Classes

- **Code Organization**: Logical grouping of related functionality
- **DRY Principle**: Reduced code duplication through inheritance
- **Flexibility**: Multiple renderers and HTTP methods per resource
- **Maintainability**: Easier to modify and extend functionality
- **Testability**: Isolated testing of individual methods

### Performance Implications

- **Instantiation Overhead**: View classes created per request
- **Memory Usage**: Instance variables consume memory
- **Caching**: Need careful consideration for cached data

### Scalability Factors

- **Database Queries**: Optimize for multiple requests
- **Caching Layers**: Implement appropriate caching strategies
- **Load Balancing**: Stateless design for horizontal scaling

### Best Practices

- **Single Responsibility**: Each view class should handle one resource type
- **Thin Controllers**: Keep business logic in separate services
- **Consistent APIs**: Follow RESTful conventions
- **Error Handling**: Comprehensive error responses
- **Documentation**: Clear API documentation

## Conclusion

Advanced view classes provide powerful patterns for building complex web applications. By leveraging multiple HTTP methods, custom predicates, and sophisticated configuration, developers can create maintainable, scalable, and feature-rich applications. Understanding these patterns enables the creation of professional-grade Pyramid applications with clean, organized code that follows web development best practices.
