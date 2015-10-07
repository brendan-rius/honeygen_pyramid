from pyramid.security import Everyone, Authenticated

import jwt


def get_user_jwt(request):
    secret_key = request.registry.settings['jwt.secret_key']
    try:
        authorization = request.headers['authorization']
    except KeyError:
        return None

    if not isinstance(authorization, str):
        try:
            authorization = authorization.decode('ascii')
        except UnicodeDecodeError:
            return None

    try:
        authmeth, auth = authorization.split(' ', 1)
    except ValueError:  # not enough values to unpack
        return None

    if authmeth.lower() == 'jwt':
        try:
            auth = jwt.decode(auth.strip(), secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None
        auth['user']['id'] = int(auth['user']['id'])  # we convert the user id into an int
        return auth['user']

    return None


class JWTAuthenticationPolicy(object):
    def authenticated_userid(self, request):
        if request.user:
            return request.user['id']

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user:
            principals += [Authenticated, 'u:%s' % user['id']]
            principals.extend(('g:%s' % g['name'] for g in user['groups']))
        return principals

    def remember(self, request, principal, **kw):
        return []

    def unauthenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user['id']
        return None
