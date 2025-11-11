# Tutorial 16: Collecting Application Info With Logging

## Overview
This tutorial demonstrates comprehensive logging implementation in Pyramid applications. Building on the view classes from tutorial 15, this tutorial shows how to collect, organize, and utilize application information through structured logging practices. You'll learn to implement logging at multiple levels, track request lifecycles, monitor performance, and handle errors effectively.

## Key Concepts

### Application Logging Fundamentals
Understanding logging levels, formats, and best practices for web applications.

### Request Lifecycle Tracking
Logging throughout the entire request-response cycle.

### Performance Monitoring
Measuring and logging response times and resource usage.

### Error Handling and Debugging
Comprehensive error logging and debugging information collection.

### Structured Logging
Consistent log formats with contextual information.

## Implementation Details

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

The logging configuration sets up the basic logging infrastructure with appropriate formatting and levels. This ensures all log messages follow a consistent structure with timestamps, logger names, and severity levels.

### Request Logger Integration

```python
def get_logger(request):
    """Add a logger to the request object."""
    return logging.getLogger('tutorial')

# In main function:
config.add_request_method(get_logger, 'logger', reify=True)
```

Adding a logger as a request method makes it easily accessible throughout the application. The `reify=True` parameter ensures the logger is created once per request and cached.

### View-Level Logging

```python
@view_defaults(route_name='home', renderer='templates/home.html')
class HomeViews:
    def __init__(self, request):
        self.request = request
        self.logger = request.logger

    @view_config(request_method='GET')
    def home(self):
        self.logger.info(f"Home page accessed from {self.request.remote_addr}")
        return {'title': 'Logging Tutorial', 'companies': list(COMPANIES.keys())}
```

Each view class initializes with a logger and logs significant events. This provides visibility into application usage patterns and helps with debugging.

### Performance Logging

```python
@view_config(request_method='GET')
def hello(self):
    start_time = time.time()
    self.logger.info(f"Hello page requested for name: {self.name}")

    result = {'name': self.name, 'greeting': f'Hello, {self.name}!'}

    end_time = time.time()
    self.logger.debug(f"Hello page rendered in {end_time - start_time:.4f} seconds")

    return result
```

Performance logging measures execution times and logs them at appropriate levels. Debug level for detailed timing, info level for general operations.

### Error Logging

```python
@view_config(request_method='POST', renderer='json')
def hello_post(self):
    try:
        data = self.request.json_body
        # Process data
        return {'result': 'processed'}
    except Exception as e:
        self.logger.error(f"Error processing POST request: {str(e)}")
        return {'error': 'Invalid request data', 'details': str(e)}
```

Error logging captures exceptions with context, helping identify and resolve issues. Both the error and a user-friendly response are logged.

### API Logging

```python
@view_config(request_method='PUT', renderer='json')
def update_company(self):
    self.logger.info(f"PUT request to update company: {self.company_name}")

    try:
        update_data = self.request.json_body
        self.logger.debug(f"Update data received: {update_data}")
        # Process update
        return {'message': 'Company updated successfully'}
    except Exception as e:
        self.logger.error(f"Error updating company {self.company_name}: {str(e)}")
        return {'error': str(e)}
```

API operations log both successful operations and failures, with debug-level logging for detailed request data.

## Logging Levels and Usage

### DEBUG Level
Used for detailed diagnostic information:

```python
self.logger.debug(f"Processing time: {end_time - start_time:.4f} seconds")
self.logger.debug(f"Received data: {data}")
```

### INFO Level
Used for general application information:

```python
self.logger.info(f"Home page accessed from {self.request.remote_addr}")
self.logger.info(f"Successfully processed request for {self.name}")
```

### WARNING Level
Used for potentially harmful situations:

```python
self.logger.warning(f"Company not found: {self.company_name}")
```

### ERROR Level
Used for serious problems:

```python
self.logger.error(f"Error processing request: {str(e)}")
```

## Request Context Logging

### Request Metadata

```python
def debug_info(self):
    debug_data = {
        'method': self.request.method,
        'url': str(self.request.url),
        'params': dict(self.request.params),
        'headers': dict(self.request.headers),
        'remote_addr': self.request.remote_addr,
        'timestamp': datetime.now().isoformat()
    }
    self.logger.debug(f"Debug data collected: {debug_data}")
    return debug_data
```

Request context logging captures comprehensive information about each request, useful for debugging and security monitoring.

### User Activity Tracking

```python
@view_config(route_name='logs', renderer='templates/logs.html')
class LogViews:
    def __call__(self):
        self.logger.info("Logs page accessed")
        # Demonstrate different log levels
        self.logger.debug("This is a debug message")
        self.logger.info("This is an info message")
        self.logger.warning("This is a warning message")
        self.logger.error("This is an error message")
```

User activity logging tracks page access and demonstrates logging level usage.

## Structured Logging Patterns

### Consistent Message Formats

```python
# Request logging
self.logger.info(f"{self.request.method} {self.request.path} from {self.request.remote_addr}")

# Operation logging
self.logger.info(f"Company {self.company_name} updated successfully")

# Error logging
self.logger.error(f"Failed to process {operation}: {str(e)}")
```

### Contextual Information

```python
log_context = {
    'user_id': self.request.authenticated_userid,
    'session_id': self.request.session.get('id'),
    'request_id': getattr(self.request, 'id', 'unknown'),
    'timestamp': datetime.now().isoformat()
}
self.logger.info(f"Operation completed", extra=log_context)
```

## Performance Monitoring

### Response Time Tracking

```python
start_time = time.time()
# Process request
result = self.process_request()
end_time = time.time()

response_time = end_time - start_time
self.logger.info(f"Request processed in {response_time:.4f} seconds")

if response_time > 1.0:  # Log slow requests
    self.logger.warning(f"Slow request detected: {response_time:.4f} seconds")
```

### Resource Usage Logging

```python
import psutil
import os

def log_resource_usage(self):
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    cpu_percent = process.cpu_percent()

    self.logger.debug(f"Memory usage: {memory_usage:.2f} MB, CPU: {cpu_percent:.1f}%")
```

## Error Handling Patterns

### Try-Catch with Logging

```python
try:
    data = self.request.json_body
    result = self.process_data(data)
    return {'success': True, 'result': result}
except json.JSONDecodeError as e:
    self.logger.warning(f"Invalid JSON received: {str(e)}")
    return {'error': 'Invalid JSON format'}
except Exception as e:
    self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return {'error': 'Internal server error'}
```

### Validation Error Logging

```python
def validate_company_data(self, data):
    errors = []
    if 'name' not in data:
        errors.append('name is required')
        self.logger.warning("Company creation failed: missing name field")

    if errors:
        self.logger.error(f"Validation failed for company data: {errors}")
        raise ValidationError(errors)
```

## Security Logging

### Authentication Events

```python
def log_authentication(self, username, success):
    if success:
        self.logger.info(f"Successful login for user: {username}")
    else:
        self.logger.warning(f"Failed login attempt for user: {username} from {self.request.remote_addr}")
```

### Access Control

```python
def check_permission(self, resource, action):
    if not self.has_permission(resource, action):
        self.logger.warning(f"Access denied: {action} on {resource} for user {self.request.authenticated_userid}")
        raise HTTPForbidden()
```

## Log Analysis and Monitoring

### Log Aggregation

```python
# Example log aggregation patterns
error_count = 0
request_count = 0

# In middleware or periodic task
def analyze_logs():
    # Count errors in last hour
    # Count requests by endpoint
    # Identify slow requests
    # Detect unusual patterns
```

### Alerting

```python
def check_error_threshold():
    recent_errors = get_recent_errors()
    if len(recent_errors) > ERROR_THRESHOLD:
        # Send alert
        self.logger.critical(f"Error threshold exceeded: {len(recent_errors)} errors in last hour")
```

## Testing Logging

### Unit Testing Log Output

```python
def test_logging():
    with mock.patch('logging.Logger.info') as mock_info:
        view = HomeViews(dummy_request)
        view.home()
        mock_info.assert_called_with("Home page accessed from 127.0.0.1")
```

### Integration Testing

```python
def test_request_logging(app):
    with mock.patch('logging.Logger.info') as mock_info:
        app.get('/')
        assert mock_info.called
        call_args = mock_info.call_args[0][0]
        assert 'Home page accessed' in call_args
```

## Configuration Management

### Environment-Based Logging

```python
import os

log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper())
logging.basicConfig(level=log_level)
```

### Structured Configuration

```ini
[logger_tutorial]
level = DEBUG
handlers = console,file
qualname = tutorial

[handler_file]
class = FileHandler
args = ('app.log',)
formatter = detailed
```

## Best Practices

### Log Message Guidelines

- Use consistent formats
- Include relevant context
- Avoid sensitive information
- Use appropriate log levels

### Performance Considerations

- Log asynchronously when possible
- Use structured logging for better parsing
- Implement log rotation
- Monitor log file sizes

### Security Considerations

- Never log passwords or sensitive data
- Sanitize user input in logs
- Implement log access controls
- Regular log review and analysis

## Analysis

### Benefits of Comprehensive Logging

- **Debugging**: Easier identification and resolution of issues
- **Monitoring**: Real-time visibility into application health
- **Security**: Tracking of suspicious activities
- **Performance**: Identification of bottlenecks and optimization opportunities
- **Auditing**: Compliance and regulatory requirements

### Logging Overhead

- **Performance Impact**: Logging operations consume resources
- **Storage Requirements**: Log files can grow quickly
- **Privacy Concerns**: Careful handling of personal data

### Implementation Patterns

- **Centralized Configuration**: Consistent logging setup across the application
- **Context Propagation**: Request IDs and user context throughout the call stack
- **Structured Data**: JSON-formatted logs for better analysis
- **Log Levels**: Appropriate use of DEBUG, INFO, WARNING, ERROR levels

### Scalability Factors

- **Log Aggregation**: Centralized logging for distributed systems
- **Asynchronous Logging**: Non-blocking log operations
- **Log Rotation**: Automatic management of log file sizes
- **Compression**: Storage optimization for historical logs

## Conclusion

Comprehensive logging is essential for modern web applications. This tutorial demonstrates how to implement logging throughout a Pyramid application, from basic request tracking to advanced performance monitoring and error handling. Effective logging practices enable better debugging, monitoring, security, and maintenance of web applications. Understanding these patterns allows developers to build more robust, observable, and maintainable systems.
