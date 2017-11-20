"""Journal security settings."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated, Allow
from pyramid.session import SignedCookieSessionFactory
from passlib.apps import custom_app_context as pwd_context


def includeme(config):
    """Security configuration."""
    auth_secret = os.environ.get("AUTH_SECRET")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg="sha512"
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    session_secret = os.environ.get('SESSION_SECRET', "")
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission("view")
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    config.set_root_factory(MyRoot)


def check_credentials(username, password):
    """Check the user login info."""
    stored_username = os.environ.get("AUTH_USERNAME", "")
    stored_password = os.environ.get("AUTH_PASSWORD", "")
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password, stored_password)
            except ValueError:
                pass
    return is_authenticated


class MyRoot(object):
    """."""

    def __init__(self, request):
        """Set up MyRoot initialization."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "secret")
    ]
