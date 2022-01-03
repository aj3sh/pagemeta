from django.db import models

# Create your models here.


class MetaForPage(models.Model):
	page_url = models.CharField('Page Url', max_length=255)
	title = models.CharField('Title', max_length=255)
	description = models.CharField('Description', max_length=255)
	image = models.ImageField('Image')
	keywords = models.CharField('Keywords', max_length=255, null=True, blank=True)

	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title

	@property
	def image_url(self):
		return '{}{}'.format('http://127.0.0.1', self.image.url)