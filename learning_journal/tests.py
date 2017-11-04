"""Functions that test server functions."""
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
