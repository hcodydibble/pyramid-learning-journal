"""Routes and URIs."""


def includeme(config):
    """Add routes and their URIs."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('details', '/journal/{id:\d+}')
    config.add_route('create', '/journal/new-entry')
    config.add_route('update', '/journal/{id:\d+}/edit-entry')
    config.add_route('delete', '/journal/{id:\d+}/delete')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
