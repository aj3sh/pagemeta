from django.db import models
from django.template.loader import render_to_string

from .requests import RequestService, get_request

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
	Also used for rendering
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

	def __str__(self):
		return self.render()

	def render(self):
		return render_to_string(template_name='pagemeta/meta.html', context={
			'meta': self,
			'request': get_request(),
		})

	@staticmethod
	def from_meta_for_page(obj):
		if obj == None:
			return None
			
		return Meta(
			title=obj.title,
			description=obj.description,
			image=obj.image,
			keywords=obj.keywords,
		)
	