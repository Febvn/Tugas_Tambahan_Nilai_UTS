from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Page,
    User,
)


# Retrieve the user's IP address from the request
def get_user(request):
    # the user could be "authenticated" by looking up the user_id
    # in the session; here we just return a hard-coded user
    user_id = request.session.get('user_id')
    if user_id:
        return DBSession.query(User).filter_by(id=user_id).first()
    return None


@view_config(route_name='home', renderer='templates/home.html')
def home_view(request):
    pages = DBSession.query(Page).order_by(Page.name)
    return dict(pages=pages)


@view_config(route_name='page', renderer='templates/page.html')
def page_view(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        raise HTTPNotFound('No such page')

    return dict(page=page,
                user=get_user(request))


@view_config(route_name='add_page', renderer='templates/edit.html',
             permission='edit')
def add_page_view(request):
    pagename = request.matchdict['pagename']
    if 'form.submitted' in request.params:
        body = request.params['body']
        page = Page(name=pagename, data=body)
        user = get_user(request)
        if user:
            page.creator_id = user.id
        DBSession.add(page)
        return HTTPFound(location=request.route_url('page',
                                                    pagename=pagename))

    save_url = request.route_url('add_page', pagename=pagename)
    page = Page(name='', data='')
    return dict(page=page, save_url=save_url, user=get_user(request))


@view_config(route_name='edit_page', renderer='templates/edit.html',
             permission='edit')
def edit_page_view(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        raise HTTPNotFound('No such page')

    if 'form.submitted' in request.params:
        page.data = request.params['body']
        user = get_user(request)
        if user:
            page.creator_id = user.id
        return HTTPFound(location=request.route_url('page',
                                                    pagename=pagename))

    return dict(page=page,
                save_url=request.route_url('edit_page',
                                           pagename=pagename),
                user=get_user(request))
