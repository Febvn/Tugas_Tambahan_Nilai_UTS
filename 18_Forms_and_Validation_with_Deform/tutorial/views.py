from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import deform
from .forms import Contact, User, SequenceForm

@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return {'title': 'Forms and Validation Demo'}

@view_config(route_name='contact', renderer='templates/contact.html')
def contact(request):
    schema = Contact()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            # Process the valid form data
            request.session.flash(f"Thank you {appstruct['name']}! Your message has been sent.", 'success')
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'Contact Form'}

    return {'form': form.render(), 'title': 'Contact Form'}

@view_config(route_name='user_form', renderer='templates/user_form.html')
def user_form(request):
    schema = User()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            # Process the valid form data
            request.session.flash(f"Welcome {appstruct['name']}! Your account has been created.", 'success')
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'User Registration'}

    return {'form': form.render(), 'title': 'User Registration'}

@view_config(route_name='sequence_form', renderer='templates/sequence_form.html')
def sequence_form(request):
    schema = SequenceForm()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            # Process the valid form data
            item_count = len(appstruct['items'])
            request.session.flash(f"Form '{appstruct['title']}' submitted with {item_count} items!", 'success')
            return HTTPFound(location=request.route_url('home'))
        except deform.ValidationFailure as e:
            return {'form': e.render(), 'title': 'Sequence Form'}

    return {'form': form.render(), 'title': 'Sequence Form'}
