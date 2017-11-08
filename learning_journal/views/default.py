"""Module that contains callable server functions."""
from pyramid.view import view_config
from pyramid.httpexceptions import (HTTPBadRequest,
                                    HTTPFound,
                                    HTTPNotFound)
from learning_journal.models.entrymodel import Entry
from pyramid.security import remember, forget
from learning_journal.security import check_credentials


@view_config(route_name="home",
             renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc()).all()
    return {
        "journals": entries
    }


@view_config(route_name="about",
             renderer="learning_journal:templates/about.jinja2")
def about_view(request):
    """Function that sends the user to the About page."""
    return{}


@view_config(route_name="details",
             renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Entry).get(post_id)
    if not post:
        raise HTTPNotFound
    return {
        "title": "Details",
        "post": post
    }


@view_config(route_name="create",
             renderer="learning_journal:templates/create.jinja2",
             permission="secret")
def create_view(request):
    """Function that generates new view."""
    if request.method == "POST":
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body']
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))
    return{}


@view_config(route_name="update",
             renderer="learning_journal:templates/update.jinja2",
             permission="secret")
def update_view(request):
    """Function that updates existing view."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Entry).get(post_id)
    if not post:
        return HTTPNotFound
    if request.method == "GET":
        return{
            "title": "Update",
            "post": post
        }
    if request.method == "POST":
        post.title = request.POST['title']
        post.body = request.POST['body']
        request.dbsession.add(post)
        request.dbsession.flush()
        return HTTPFound(request.route_url('details', id=post.id))


@view_config(route_name="delete", permission="secret")
def delete_entry(request):
    """Function to delete an entry."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Entry).get(post_id)
    if not post:
        return HTTPNotFound
    request.dbsession.delete(post)
    return HTTPFound(request.route_url('home'))


@view_config(route_name="login",
             renderer="learning_journal:templates/login.jinja2",
             require_csrf=False)
def login_view(request):
    """Function to return view for login page."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    """Function to log a user out."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
