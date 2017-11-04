"""Functions that test server functions."""
import pytest
from pyramid.httpexceptions import HTTPBadRequest
from datetime import datetime
from learning_journal.models import Entry


def test_list_view_returns_list_of_entries_in_dict(dummy_request):
    """Test for the list_view function."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'journals' in response
    assert isinstance(response['journals'], list)


def test_adding_to_dummy_db_works(dummy_request):
    """Test that adding to dummy db works."""
    assert len(dummy_request.dbsession.query(Entry).all()) == 0
    test_entry = Entry(
        title="Fake Title",
        creation_date=datetime.now(),
        body="The body lul"
    )
    dummy_request.dbsession.add(test_entry)
    assert len(dummy_request.dbsession.query(Entry).all()) == 1


def test_list_view_returns_a_dict(dummy_request):
    """Function to test if list_view returns a dict."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_proper_amount_of_content(dummy_request):
    """Home view response has content."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry).all()
    assert len(response["journals"]) == len(query)


def test_about_view_returns_a_dict(dummy_request):
    """Test that about view returns dict."""
    from learning_journal.views.default import about_view
    response = about_view(dummy_request)
    assert isinstance(response, dict)


def test_create_view_returns_a_dict(dummy_request):
    """Test that create view returns dict."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert isinstance(response, dict)


def test_detail_view_returns_post_detail(dummy_request):
    """Test that detail view returns post details."""
    from learning_journal.views.default import detail_view
    test_entry = Entry(
        title="Fake Title",
        creation_date=datetime.now(),
        body="The body lul"
    )
    dummy_request.dbsession.add(test_entry)
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['post'].title == "Fake Title"


def test_create_view_get_empty_is_empty_dict(dummy_request):
    """Test that GET request on create view returns empty dict."""
    from learning_journal.views.default import create_view
    dummy_request.method = "GET"
    response = create_view(dummy_request)
    assert response == {}


def test_create_view_post_works(dummy_request):
    """Test that create view post creates new entry."""
    from learning_journal.views.default import create_view
    dummy_request.method = "POST"
    test_post = {"title": "Test", "body": "This is a body."}
    dummy_request.POST = test_post
    response = create_view(dummy_request)
    assert response.status_code == 302


def test_create_view_raises_bad_request(dummy_request):
    """Test that an incomplete post request returns HTTPBadRequest."""
    from learning_journal.views.default import create_view
    dummy_request.method = "POST"
    test_post = {"title": "Test"}
    dummy_request.POST = test_post
    with pytest.raises(HTTPBadRequest):
        create_view(dummy_request)


def test_new_entry_redirects_to_home_page(testapp, empty_db):
    """Test that after adding a new entry you get redirected to home page."""
    test_entry = {
        "title": "Fake Title",
        "body": "The body lul"
    }
    response = testapp.post("/journal/new-entry", test_entry)
    assert response.location == "http://localhost/"


def test_detail_view_returns_correct_post_title(dummy_request):
    """Test that the detail view returns the correct post."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert "Day 1: " in response['post'].title
