"""Functions that test server functions."""
import pytest


@pytest.fixture
def dummy_request():
    from pyramid import testing
    return testing.DummyRequest()


def test_list_view_returns_html(dummy_request):
    """Function to test if list_view returns proper html file."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert response.content_type == 'text/html'


def test_list_view_returns_200(dummy_request):
    """Function to test if list_view returns proper html file."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert response.status_code == 200


def test_detail_view_returns_html(dummy_request):
    """Function to test if detail_view returns proper html file."""
    from learning_journal.views.default import detail_view
    response = detail_view(dummy_request)
    assert response.content_type == 'text/html'


def test_detail_view_returns_200(dummy_request):
    """Function to test if detail_view returns proper html file."""
    from learning_journal.views.default import detail_view
    response = detail_view(dummy_request)
    assert response.status_code == 200


def test_create_view_returns_html(dummy_request):
    """Function to test if create_view returns proper html file."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert response.content_type == 'text/html'


def test_create_view_returns_200(dummy_request):
    """Function to test if create_view returns proper html file."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert response.status_code == 200


def test_update_view_returns_html(dummy_request):
    """Function to test if update_view returns proper html file."""
    from learning_journal.views.default import update_view
    response = update_view(dummy_request)
    assert response.content_type == 'text/html'


def test_update_view_returns_200(dummy_request):
    """Function to test if update_view returns proper html file."""
    from learning_journal.views.default import update_view
    response = update_view(dummy_request)
    assert response.status_code == 200


def test_about_view_returns_html(dummy_request):
    """Function to test if about_view returns proper html file."""
    from learning_journal.views.default import about_view
    response = about_view(dummy_request)
    assert response.content_type == 'text/html'


def test_about_view_returns_200(dummy_request):
    """Function to test if about_view returns proper html file."""
    from learning_journal.views.default import about_view
    response = about_view(dummy_request)
    assert response.status_code == 200
