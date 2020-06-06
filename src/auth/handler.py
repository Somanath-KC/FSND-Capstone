import json, os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = [os.environ.get('ALGORITHMS')]
API_AUDIENCE = os.environ.get('API_AUDIENCE')


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'error': 401,
            'message': 'Missing authorization header.'
        }, 401)

    parts = auth_header.split(' ')
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'error': 401,
            'message': 'Authorization must contain bearer.'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'error': 401,
            'message': 'Invalid authorization header.'
        }, 401)

    token = parts[1]
    return token


#  Check Permissions
def check_permissions(permission, payload):
    if not payload.get('permissions'):
        raise AuthError({
            'error': 401,
            'message': 'No Permissions Found.'
        }, 401)

    if permission not in payload.get('permissions'):
        raise AuthError({
            'error': 401,
            'message': 'Not permitted.'
        }, 401)

#  Verify JWT
def verify_decode_jwt(token):
    url = 'https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)
    json_url = urlopen(url)
    jwks = json.loads(json_url.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except:
        raise AuthError({
            'error': 401,
            'message': 'Invalid Token'
        }, 401)

    rsa_key = {}
    
    if 'kid' not in unverified_header:
        raise AuthError({
            'error': 401,
            'message': 'Invalid authorization header.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://{}/'.format(AUTH0_DOMAIN)
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
            'error': 401,
            'message': 'Token Expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
            'error': 401,
            'message': 'Invalid Claims.'
            }, 401)

        except Exception:
            raise AuthError({
            'error': 401,
            'message': 'Invalid headers.'
        }, 401)
    else:
        raise AuthError({
            'error': 401,
            'message': 'Invalid headers unable to find appropriate keys.'
        }, 401)
    

# Requires auth decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator