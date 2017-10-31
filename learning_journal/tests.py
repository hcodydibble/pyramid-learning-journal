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
