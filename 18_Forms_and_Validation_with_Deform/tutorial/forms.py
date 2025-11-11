import colander  # type: ignore
import deform.widget  # type: ignore

class Contact(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Name", description="Your full name", validator=colander.Length(min=2, max=100))  # type: ignore[reportCallIssue]
    email = colander.SchemaNode(colander.String(), title="Email", description="Your email address", validator=colander.Email())  # type: ignore[reportCallIssue]
    message = colander.SchemaNode(colander.String(), title="Message", description="Your message", widget=deform.widget.TextAreaWidget(rows=10), validator=colander.Length(min=10, max=1000))  # type: ignore[reportCallIssue]

class Person(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())  # type: ignore[reportCallIssue]
    age = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 200))  # type: ignore[reportCallIssue]

class People(colander.SequenceSchema):
    person = Person()

class Conference(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())  # type: ignore[reportCallIssue]
    attendees = People()

class DateRange(colander.MappingSchema):
    start = colander.SchemaNode(colander.Date(), title="Start Date")  # type: ignore[reportCallIssue]
    end = colander.SchemaNode(colander.Date(), title="End Date")  # type: ignore[reportCallIssue]

class User(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Full Name", description="Please enter your full name", validator=colander.Length(min=3, max=100))  # type: ignore[reportCallIssue]
    age = colander.SchemaNode(colander.Integer(), title="Age", description="Your age in years", validator=colander.Range(min=13, max=120), widget=deform.widget.TextInputWidget(size=3))  # type: ignore[reportCallIssue]
    email = colander.SchemaNode(colander.String(), title="Email Address", description="We promise not to spam you", validator=colander.Email())  # type: ignore[reportCallIssue]
    password = colander.SchemaNode(colander.String(), title="Password", description="Choose a strong password", validator=colander.Length(min=8), widget=deform.widget.PasswordWidget())  # type: ignore[reportCallIssue]
    confirm_password = colander.SchemaNode(colander.String(), title="Confirm Password", widget=deform.widget.PasswordWidget())  # type: ignore[reportCallIssue]
    interests = colander.SchemaNode(colander.Set(), title="Interests", description="Select all that apply", widget=deform.widget.CheckboxChoiceWidget(values=[('sports', 'Sports'), ('music', 'Music'), ('travel', 'Travel'), ('reading', 'Reading'), ('cooking', 'Cooking'), ('technology', 'Technology')]))  # type: ignore[reportCallIssue]
    country = colander.SchemaNode(colander.String(), title="Country", widget=deform.widget.SelectWidget(values=[('', '-- Select Country --'), ('us', 'United States'), ('ca', 'Canada'), ('uk', 'United Kingdom'), ('de', 'Germany'), ('fr', 'France'), ('jp', 'Japan'), ('au', 'Australia'), ('other', 'Other')]))  # type: ignore[reportCallIssue]
    bio = colander.SchemaNode(colander.String(), title="Biography", description="Tell us about yourself (optional)", missing="", widget=deform.widget.TextAreaWidget(rows=5, cols=60))  # type: ignore[reportCallIssue]
    newsletter = colander.SchemaNode(colander.Boolean(), title="Subscribe to Newsletter", description="Receive updates and news", missing=False)  # type: ignore[reportCallIssue]

    def validator(self, node, cstruct):
        """Custom validator for password confirmation."""
        if cstruct.get('password') != cstruct.get('confirm_password'):
            raise colander.Invalid(node, "Passwords do not match")

class SequenceItem(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), title="Name")  # type: ignore[reportCallIssue]
    value = colander.SchemaNode(colander.Integer(), title="Value")  # type: ignore[reportCallIssue]

class SequenceForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), title="Form Title", description="Give this form a title")  # type: ignore[reportCallIssue]
    items = colander.SchemaNode(colander.Sequence(), SequenceItem(), title="Items", description="Add multiple items", validator=colander.Length(min=1, max=10), widget=deform.widget.SequenceWidget(min_len=1, max_len=10))  # type: ignore[reportCallIssue]
