from __future__ import absolute_import, print_function, unicode_literals


def exposed(cls):
    resource_item, resource_collection = cls.resource_subtree()
    all_models[cls] = {
        'resource_collection': resource_collection,
        'resource_item': resource_item,
    }
    return cls


all_models = {}
