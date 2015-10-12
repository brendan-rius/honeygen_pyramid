from __future__ import absolute_import, print_function, unicode_literals
from pyramid.view import view_config


class NotFoundException(Exception):
    def __init__(self, cls, id):
        super().__init__('Cannot find {} identified by "{}"'.format(cls.hg_name(), id))
        self.code = 404


@view_config(context=NotFoundException, renderer='json')
def exception_view(exc, request):
    request.response.status_code = exc.code
    return {
        'errors': [
            {
                'status': str(exc.code),
                'detail': str(exc),
            },
        ],
    }
