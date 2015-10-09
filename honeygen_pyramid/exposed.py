from __future__ import absolute_import, print_function, unicode_literals


def exposed(cls):
    """
    An annotation that represents a model that should be exposed through the API.
    This annotation allows models to be registered (and thus accessed by the code that
    need them), and to cache information about the models.
    :param cls: the model class
    :return: the model class
    """
    # We generate the resource classes dynamically for the model, and store them as well
    # as the class into a global, because we do not want to re-create different classes
    # each time (they won't be equal), and we do not want to loose time constructing them
    # each time
    resource_item, resource_collection = cls.hg_resource_subtree()
    # We generate the view classes dynamically
    item_view, collection_view = cls.hg_get_views(resource_collection, resource_item)
    all_models[cls] = {
        'resource_collection': resource_collection,
        'resource_item': resource_item,
        'name': cls.hg_name(),
        'pluralized_name': cls.hg_pluralized_name(),
        'url': cls.hg_url(),
        'item_view': item_view,
        'collection_view': collection_view,
    }
    return cls


all_models = {}
