"""Journal security settings."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated
from pyramid.security import Allow
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
    config.set_authorization_policy(authz_policy)
    config.set_default_permission("view")
    config.set_root_factory(MyRoot)


def check_credentials(username, password):
    """Check the user login info."""
    stored_username = os.environ.get("AUTH_USERNAME", "")
    sotred_password = os.environ.get("AUTH_PASSWORD", "")
    is_authenticated = False
    if stored_username and stored_username:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password, sotred_password)
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
