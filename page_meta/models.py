import sys
from django.db import models

# Create your models here.

TESTING = sys.argv[1:2] == ['test']
TESTING_PATH = '/test'

class RequestService:

	@property
	def request(self):
		if not hasattr(self, '__request'):
			self.__request = self.__class__._get_request()
		return self.__request

	@property
	def root_url(self):
		if TESTING:
			# for testing
			return 'http://localhost:8000'
		if not hasattr(self, '__root_url'):
			self.__root_url = '{}://{}'.format(self.request.scheme, self.request.get_host())
		return self.__root_url

	@property
	def path(self):
		if TESTING:
			# for testing
			return TESTING_PATH
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

	@staticmethod
	def _get_request():
		import sys
		f = sys._getframe()
		while f:
			request = f.f_locals.get("request")
			if request:
				return request
			f = f.f_back
		return None


class MetaForPage(models.Model):
	page_url = models.CharField('Page Url', max_length=255, help_text='Enter the relative url eg. /contact-us. To use as the default enter "DEFAULT".')
	title = models.CharField('Title', max_length=255)
	description = models.CharField('Description', max_length=255)
	image = models.ImageField('Image')
	keywords = models.CharField('Keywords', max_length=255, null=True, blank=True)

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.title

	@property
	def image_url(self):
		request_service = RequestService()
		return request_service.get_full_url(path=self.image.url)
	
	@classmethod
	def get_default_meta(cls):
		if cls.objects.filter(page_url__iexact='default').exists():
			return cls.objects.filter(page_url__iexact='default').first()
		return None
	
	@classmethod
	def get_meta_from_current_url(cls):
		request_service = RequestService()
		qs = cls._default_manager.filter(
			models.Q(page_url=request_service.path) |
			models.Q(page_url=request_service.full_path)
		)
		return qs.first()

class Meta:
	'''
	Plain model for storing title description image keywords
	'''

	class Image:
		DEFAULT_WIDTH = 1200
		DEFAULT_HEIGHT = 800

		def __init__(self, url, width=None, height=None) -> None:
			self.url, self.width, self.height = url, width, height
			if self.width == None: self.width = self.DEFAULT_WIDTH
			if self.height == None: self.height = self.DEFAULT_HEIGHT


	def __init__(self, title, description, image=None, image_url=None, image_width=None, image_height=None, keywords=None):
		self.title = title
		self.description = description
		self.keywords = keywords
		
		if image == None and image_url == None:
			raise ValueError('Both image or image_url cannot be empty.')

		request_service = RequestService()
		if image != None:
			self.image = image
			self.image_url = request_service.get_full_url(path=self.image.url)
		else:
			self.image_url = request_service.get_full_url(path=image_url)
			self.image = Meta.Image(url=image_url, width=image_width, height=image_height)

