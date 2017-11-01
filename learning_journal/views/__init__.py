from .default import list_view, detail_view, create_view, update_view, about_view


def includeme(config):
    """."""
    config.add_view(list_view, route_name='home')
    config.add_view(detail_view, route_name='details')
    config.add_view(create_view, route_name='create')
    config.add_view(update_view, route_name='update')
    config.add_view(about_view, route_name='about')
