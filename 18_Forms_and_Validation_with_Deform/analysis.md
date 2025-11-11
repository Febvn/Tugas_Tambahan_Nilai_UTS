# Tutorial 18: Forms and Validation with Deform

## Overview

This tutorial demonstrates how to create robust web forms using Deform, a Python HTML form generation library built on top of Colander (a data validation and deserialization library). Deform provides a comprehensive solution for form generation, validation, and rendering in Pyramid applications.

## Key Concepts

### What is Deform?

Deform is a Python library for generating HTML forms from schemas defined using Colander. It provides:

- **Schema-based form generation**: Forms are defined using Python schemas
- **Automatic validation**: Client and server-side validation
- **Widget system**: Rich set of form widgets (text inputs, checkboxes, selects, etc.)
- **Bootstrap integration**: Built-in Bootstrap CSS framework support
- **Extensible architecture**: Custom widgets and validators

### Colander Schema System

Colander provides data validation and deserialization:

- **Schema nodes**: Define data types and validation rules
- **Validators**: Built-in and custom validation functions
- **Serialization/Deserialization**: Convert between Python objects and external representations
- **Error handling**: Comprehensive error reporting

## Implementation Details

### Application Configuration

The application includes Deform static resources and configures Jinja2 templating:

```python
config.add_static_view('deform_static', 'deform:static/')
config.include('pyramid_jinja2')
config.add_jinja2_renderer('.html')
```

### Schema Definitions

#### Contact Form Schema
```python
class Contact(colander.MappingSchema):
    name = colander.SchemaNode(
        colander.String(),
        title="Name",
        description="Your full name",
        validator=colander.Length(min=2, max=100)
    )
    email = colander.SchemaNode(
        colander.String(),
        title="Email",
        description="Your email address",
        validator=colander.Email()
    )
    message = colander.SchemaNode(
        colander.String(),
        title="Message",
        description="Your message",
        widget=deform.widget.TextAreaWidget(rows=10),
        validator=colander.Length(min=10, max=1000)
    )
```

#### User Registration Schema
```python
class User(colander.MappingSchema):
    name = colander.SchemaNode(
        colander.String(),
        title="Full Name",
        validator=colander.Length(min=3, max=100)
    )
    age = colander.SchemaNode(
        colander.Integer(),
        title="Age",
        validator=colander.Range(min=13, max=120)
    )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email()
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=8),
        widget=deform.widget.PasswordWidget()
    )
    confirm_password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget()
    )

    def validator(self, node, cstruct):
        if cstruct.get('password') != cstruct.get('confirm_password'):
            raise colander.Invalid(node, "Passwords do not match")
```

#### Sequence Form Schema
```python
class SequenceItem(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Name")
    value = colander.SchemaNode(colander.Integer(), title="Value")

class SequenceForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), title="Form Title")
    items = colander.SchemaNode(
        colander.Sequence(),
        SequenceItem(),
        title="Items",
        widget=deform.widget.SequenceWidget(min_len=1, max_len=10)
    )
```

### Form Processing

#### Basic Form Handling
```python
@view_config(route_name='contact', renderer='templates/contact.html')
def contact(request):
    schema = Contact()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            # Process valid form data
            request.session.flash("Thank you for your message!", 'success')
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render()}

    return {'form': form.render()}
```

### Widget Types

#### Text Input Widgets
- `TextInputWidget`: Basic text input
- `TextAreaWidget`: Multi-line text input
- `PasswordWidget`: Password input (masked)
- `HiddenWidget`: Hidden form field

#### Selection Widgets
- `SelectWidget`: Dropdown selection
- `RadioChoiceWidget`: Radio button selection
- `CheckboxChoiceWidget`: Multiple checkbox selection
- `CheckboxWidget`: Single checkbox

#### Sequence Widgets
- `SequenceWidget`: Dynamic list with add/remove functionality

#### Date/Time Widgets
- `DateInputWidget`: Date picker
- `DateTimeInputWidget`: Date and time picker

### Validation Types

#### Built-in Validators
- `Length(min, max)`: String length validation
- `Range(min, max)`: Numeric range validation
- `Email()`: Email format validation
- `Regex(pattern)`: Regular expression validation
- `OneOf(choices)`: Value must be in list
- `NoneOf(choices)`: Value must not be in list

#### Custom Validators
```python
def custom_validator(node, value):
    if not value.startswith('prefix_'):
        raise colander.Invalid(node, "Value must start with 'prefix_'")

class CustomSchema(colander.MappingSchema):
    field = colander.SchemaNode(
        colander.String(),
        validator=custom_validator
    )
```

### Error Handling

#### Validation Failure
```python
try:
    appstruct = form.validate(controls)
except deform.ValidationFailure as e:
    # Form validation failed
    return {'form': e.render()}
```

#### Custom Error Messages
```python
name = colander.SchemaNode(
    colander.String(),
    validator=colander.Length(min=2, max=100),
    title="Name",
    description="Enter your full name",
    missing_msg="Name is required",
    too_short="Name must be at least ${min} characters",
    too_long="Name must be at most ${max} characters"
)
```

## Features Implemented

### 1. Contact Form
- Basic form with name, email, and message fields
- Server-side validation
- Success/error messaging with flash messages
- Bootstrap-styled form rendering

### 2. User Registration Form
- Comprehensive registration form
- Password confirmation validation
- Multiple input types (text, email, password, select, checkboxes)
- Age validation with range checking
- Interest selection with checkboxes
- Country dropdown
- Optional biography field

### 3. Sequence Form
- Dynamic form with add/remove functionality
- Multiple items with name-value pairs
- Minimum and maximum item limits
- Individual item validation

### 4. Form Validation
- Client-side validation feedback
- Server-side validation with detailed error messages
- Custom validation rules (password confirmation)
- Real-time validation feedback

### 5. User Interface
- Responsive Bootstrap-based design
- Form field highlighting and focus states
- Error and success state styling
- Password strength indicator
- Loading states during form submission

## Technical Implementation

### View Functions

#### Contact Form View
```python
@view_config(route_name='contact', renderer='templates/contact.html')
def contact(request):
    schema = Contact()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            request.session.flash(
                f"Thank you {appstruct['name']}! Your message has been sent.",
                'success'
            )
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'Contact Form'}

    return {'form': form.render(), 'title': 'Contact Form'}
```

#### User Form View
```python
@view_config(route_name='user_form', renderer='templates/user_form.html')
def user_form(request):
    schema = User()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            request.session.flash(
                f"Welcome {appstruct['name']}! Your account has been created.",
                'success'
            )
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'User Registration'}

    return {'form': form.render(), 'title': 'User Registration'}
```

#### Sequence Form View
```python
@view_config(route_name='sequence_form', renderer='templates/sequence_form.html')
def sequence_form(request):
    schema = SequenceForm()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            item_count = len(appstruct['items'])
            request.session.flash(
                f"Form '{appstruct['title']}' submitted with {item_count} items!",
                'success'
            )
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'Sequence Form'}

    return {'form': form.render(), 'title': 'Sequence Form'}
```

### Template Integration

#### Form Rendering
```html
<div class="form-container">
    {{ form|safe }}
</div>
```

#### Flash Messages
```html
{% for message in request.session.pop_flash() %}
<div class="alert alert-{{ 'success' if 'success' in message.category else 'danger' }}">
    {{ message }}
</div>
{% endfor %}
```

### JavaScript Enhancements

#### Form Validation
```javascript
function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(input.value);

    if (input.value && !isValid) {
        showFieldError(input, 'Please enter a valid email address');
    }
}

function validatePasswordStrength(input) {
    // Password strength calculation and visual feedback
}
```

## Security Considerations

### Form Security
- CSRF protection through Pyramid's built-in CSRF support
- Input sanitization through Colander validation
- Password field masking
- Secure session handling for flash messages

### Validation Security
- Server-side validation as primary defense
- Client-side validation for user experience
- Input length limits to prevent buffer overflows
- Email validation to prevent malformed data

## Best Practices

### Schema Design
- Use descriptive field titles and descriptions
- Provide helpful error messages
- Set appropriate validation constraints
- Use appropriate widget types for data types

### Form Handling
- Always validate on server side
- Handle validation failures gracefully
- Provide clear success/error feedback
- Use appropriate HTTP redirects after successful submission

### User Experience
- Provide real-time validation feedback
- Use appropriate input types (email, number, etc.)
- Group related fields logically
- Provide helpful placeholder text and descriptions

## Advanced Features

### Custom Widgets
```python
class CustomWidget(deform.widget.Widget):
    def serialize(self, field, cstruct, **kw):
        # Custom serialization logic
        pass

    def deserialize(self, field, pstruct):
        # Custom deserialization logic
        pass
```

### Custom Validators
```python
def unique_username_validator(node, value):
    # Check database for unique username
    if not is_username_unique(value):
        raise colander.Invalid(node, "Username already exists")

class RegistrationSchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=unique_username_validator
    )
```

### Form Pre-population
```python
# Pre-populate form with existing data
form = deform.Form(schema, buttons=('submit',))
appstruct = {'name': 'John Doe', 'email': 'john@example.com'}
form_rendered = form.render(appstruct)
```

### File Upload Handling
```python
import colander
import deform.widget

class FileUpload(colander.MappingSchema):
    file = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget()
    )
```

## Testing the Application

1. **Start the application**:
   ```bash
   cd 18_Forms_and_Validation_with_Deform
   pserve development.ini
   ```

2. **Test contact form**:
   - Visit http://localhost:6543/contact
   - Try submitting with missing fields
   - Try invalid email format
   - Submit valid form

3. **Test user registration**:
   - Visit http://localhost:6543/user
   - Test password confirmation
   - Try different validation scenarios
   - Submit complete form

4. **Test sequence form**:
   - Visit http://localhost:6543/sequence
   - Add and remove items
   - Test validation on individual items
   - Submit form with multiple items

5. **Test validation feedback**:
   - Observe real-time validation
   - Check error message styling
   - Verify success states

## Performance Considerations

- Deform forms are rendered server-side
- Static assets (CSS/JS) should be cached
- Large forms may benefit from pagination
- Sequence widgets can impact performance with many items

## Conclusion

This tutorial demonstrates comprehensive form handling with Deform and Colander in Pyramid applications. The implementation showcases:

- Schema-based form definition
- Comprehensive validation
- Rich widget ecosystem
- Professional UI with Bootstrap
- Client-side enhancements
- Security best practices
- User experience optimization

Deform provides a powerful, flexible system for building complex web forms with robust validation, making it an excellent choice for Pyramid applications requiring sophisticated form handling.
