"""Decorators for tests."""
import pytest


@pytest.fixture
def dummy_request():
    from pyramid import testing
    return testing.DummyRequest()
