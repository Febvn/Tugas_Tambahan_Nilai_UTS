# Tutorial 11: Dispatching URLs To Views With Routing

## Overview
This tutorial introduces Pyramid's URL routing system, which maps URLs to view functions. Routing allows for clean, meaningful URLs and separates URL structure from view logic.

## Key Concepts

### Route Configuration
Routes map URL patterns to named routes that can be referenced in views.

### URL Parameters
Extracting dynamic values from URLs using route patterns.

### HTTP Exceptions
Using Pyramid's exception classes for redirects and error responses.

## Implementation Details

### Route Definition
```python
config.add_route('home', '/')
config.add_route('hello', '/howdy/{name}')
config.add_route('redirect', '/goto')
config.add_route('gone', '/gone')
```

### Parameter Extraction
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

## Route Patterns

### Static Routes
Simple routes that match exact URLs.

### Dynamic Routes
Routes with placeholders for variable parts.

### Optional Parameters
Routes with optional path segments.

### Regular Expression Routes
Advanced pattern matching with regex.

## URL Generation

### Route URLs
Generating URLs from route names and parameters.

### Reverse Routing
Creating URLs programmatically instead of hardcoding.

### URL Building
Constructing URLs with query parameters and fragments.

## Route Matching

### Pattern Matching
How Pyramid matches URLs to routes.

### Precedence
Order of route evaluation.

### Fallback Routes
Default routes for unmatched URLs.

## HTTP Exceptions

### Redirects
HTTPFound for temporary redirects.

### Permanent Redirects
HTTPMovedPermanently for permanent moves.

### Error Responses
HTTPNotFound, HTTPForbidden, etc.

### Custom Exceptions
Creating application-specific exceptions.

## Advanced Routing

### Route Predicates
Filtering routes based on conditions.

### Custom Route Factories
Advanced route configuration.

### Subdomain Routing
Routing based on subdomain.

### Internationalization
Localized URL routing.

## Analysis

### Routing vs Traversal
URL dispatch vs object traversal approaches.

### RESTful URLs
Designing clean, meaningful URL structures.

### SEO Considerations
URL structure impact on search engine optimization.

### Security Implications
Avoiding URL-based attacks through proper routing.

### Performance
Route matching efficiency and caching.

## Best Practices

### URL Design
- Use descriptive, hierarchical URLs
- Keep URLs short and memorable
- Use lowercase with hyphens for readability
- Avoid query parameters when possible

### Route Organization
- Group related routes logically
- Use consistent naming conventions
- Document route purposes
- Plan for future URL changes

### Error Handling
- Use appropriate HTTP status codes
- Provide meaningful error messages
- Handle edge cases gracefully
- Log errors for debugging

### Testing
- Test all route variations
- Verify parameter extraction
- Check error conditions
- Validate URL generation

## Conclusion
URL routing is a fundamental aspect of web application development. Pyramid's routing system provides powerful tools for creating clean, maintainable URL structures that enhance both user experience and application architecture. Understanding routing patterns and HTTP exceptions enables developers to build robust web applications with proper URL handling and error management.
