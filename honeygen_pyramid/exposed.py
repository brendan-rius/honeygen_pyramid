from __future__ import absolute_import, print_function, unicode_literals


def exposed(cls):
    all_models.append(cls)
    return cls


all_models = []
