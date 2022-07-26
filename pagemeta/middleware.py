from threading import current_thread
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

from pagemeta.utils import get_meta, set_meta

_requests = {}

class MetaRequestMiddleware(MiddlewareMixin):
    '''
    stores current request in the current thread.
    removes the saved request after the response is complete
    '''
    def process_request(self, request):
        # storing request using current thread as a key
        _requests[current_thread().ident] = request
        
    def process_response(self, request, response):
        # when response is ready, request should be flushed
        _requests.pop(current_thread().ident, None)
        return response

    def process_exception(self, request, exception):
        # if an exception has happened, request should be flushed too
         _requests.pop(current_thread().ident, None)


# binding meta property in request
HttpRequest.meta = property(get_meta, set_meta)
