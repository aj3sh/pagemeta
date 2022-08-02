import sys
from threading import current_thread

from .middleware import _requests

def get_request():
    '''
    returns request saved using current thread as a key
    '''
    current_thread_ident = current_thread().ident
    if current_thread_ident not in _requests:
        raise ImportError('Unable to retrieve request. Make sure "pagemeta.middleware.MetaRequestMiddleware" is '
            'added in your settings and working properly.')
    return _requests.get(current_thread_ident, None)

class RequestService:

	@property
	def request(self):
		if not hasattr(self, '__request'):
			self.__request = get_request()
		return self.__request

	@property
	def root_url(self):
		if not hasattr(self, '__root_url'):
			self.__root_url = '{}://{}'.format(self.request.scheme, self.request.get_host())
		return self.__root_url

	@property
	def path(self):
		return self.request.path

	@property
	def full_path(self):
		return self.get_full_url(self.path)

	def get_full_url(self, path):
		if 'http://' in path or 'https://' in path:
			return path
		elif not path.startswith('/'):
			path = '/'+path
		return '{}{}'.format(self.root_url, path)


