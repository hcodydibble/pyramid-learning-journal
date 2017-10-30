def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('single_entry', '/journal/{id:\d+}')
    config.add_route('create', '/journal/new-entry')
    config.add_route('edit', '/journal/{id:\d+}/edit-entry')
