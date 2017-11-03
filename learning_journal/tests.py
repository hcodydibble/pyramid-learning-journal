"""Functions that test server functions."""
from learning_journal.data.journal_entries import JOURNAL_ENTRIES
import pytest


@pytest.fixture
def testapp():
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_list_view_returns_a_dict(dummy_request):
    """Function to test if list_view returns a dict."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_proper_amount_of_content(dummy_request):
    """Home view response has content."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response["journals"]) == len(JOURNAL_ENTRIES)


def test_about_view_returns_a_dict(dummy_request):
    """Test that detail view returns html."""
    from learning_journal.views.default import about_view
    response = about_view(dummy_request)
    assert isinstance(response, dict)


def test_create_view_returns_a_dict(dummy_request):
    """Test that detail view returns html."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert isinstance(response, dict)


def test_layout_root(testapp):
    """Test that the contents of the root page contains <article>."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Your Website 2017' in html.find("footer").text


def test_detail_view_returns_correct_title(testapp):
    """Test that the title of a chosen entry gets returned."""
    response = testapp.get("/journal/3", status=200)
    html = response.html
    assert "Day Three: Another day. Another knowledge." in html.find("h2").text


def test_update_view_returns_a_form(testapp):
    """Test that the title of a chosen entry gets returned."""
    response = testapp.get("/journal/3/edit-entry", status=200)
    html = response.html
    assert html.find("form")
