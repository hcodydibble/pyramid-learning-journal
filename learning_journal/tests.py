"""Functions that test server functions."""
import pytest
import transaction
from pyramid import testing
from learning_journal.models import (
    Entry,
    get_tm_session
)
from learning_journal.models.meta import Base
from faker import Faker
from datetime import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test_db'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture(scope="session")
def testapp(request):
    """Test function for mimicking working site."""
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{"sqlalchemy.url": "postgres://localhost:5432/test_db"})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill out a database."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(ENTRIES)

    return dbsession

FAKE = Faker()
ENTRIES = [Entry(
    title="Day {}: {}".format(i + 1, FAKE.text(30)),
    creation_date=FAKE.date_time,
    body=FAKE.paragraph()
) for i in range(20)]


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


def test_home_route_with_journals_has_headers(testapp, fill_the_db):
    """Test that the home route lists out journal entries."""
    response = testapp.get("/")
    assert len(response.html.find_all('h2')) == 20


def test_detail_view_returns_correct_post_title(dummy_request):
    """Test that the detail view returns the correct post."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert "Day 1: " in response['post'].title
