from django_cognito_jwt import JSONWebTokenAuthentication

import logging
log = logging.getLogger(__name__)

log.debug("HEYT")
class TESTJWT(JSONWebTokenAuthentication):
    def authenticate(self, request):
        log.debug(f'REQUEST: {request}')
        return super(TESTJWT, self).authenticate(request)

    def get_jwt_token(self, request):
        log.deubg(f'JWT {request}')
        return super(TESTJWT, self).get_jwt_token(request)
