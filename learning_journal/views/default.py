"""Module that contains callable server functions."""
from pyramid.view import view_config
from learning_journal.data.journal_entries import JOURNAL_ENTRIES


@view_config(route_name="home", renderer="learning_journal:templates/journal_entries.jinja2")
def list_view(request):
    """Function that generates list of journal entries."""
    return {
        "journals": JOURNAL_ENTRIES[::-1]
    }


@view_config(route_name="about", renderer="learning_journal:templates/about.jinja2")
def about_view(request):
    """Function that sends the user to the About page."""
    return{
        "title": "This is what I do."
    }


@view_config(route_name="details", renderer="learning_journal:templates/details.jinja2")
def detail_view(request):
    """Function that generates single journal entry."""
    post_id = int(request.matchdict['id'])
    post = list(filter(lambda post: post['id'] == post_id, JOURNAL_ENTRIES))[0]
    return {
        "title": "Details",
        "post": post
    }


@view_config(route_name="create", renderer="learning_journal:templates/create.jinja2")
def create_view(request):
    """Function that generates new view."""
    return{
        "title": "Make many much words."
    }


@view_config(route_name="update", renderer="learning_journal:templates/update.jinja2")
def update_view(request):
    """Function that updates existing view."""
    post_id = int(request.matchdict['id'])
    post = list(filter(lambda post: post['id'] == post_id, JOURNAL_ENTRIES))[0]
    return{
        "title": "Update",
        "post": post
    }
    pass
