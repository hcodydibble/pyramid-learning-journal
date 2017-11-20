"""Module that contains callable server functions."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound, HTTPNotFound
from learning_journal.models.entrymodel import Entry


@view_config(route_name="home", renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc()).all()
    return {
        "journals": entries
    }


@view_config(route_name="about", renderer="learning_journal:templates/about.jinja2")
def about_view(request):
    """Function that sends the user to the About page."""
    return{}


@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Entry).get(post_id)
    if post:
        return {
            "title": "Details",
            "post": post
        }
    raise HTTPNotFound


@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
def create_view(request):
    """Function that generates new view."""
    if request.method == "GET":
        return{}
    if request.method == "POST":
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body']
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))


@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
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


@view_config(route_name="delete")
def delete_entry(request):
    """Function to delete an entry."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Entry).get(post_id)
    if not post:
        return HTTPNotFound
    request.dbsession.delete(post)
    return HTTPFound(request.route_url('home'))
