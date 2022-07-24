from ast import keyword
from django.test import TestCase

from page_meta.requests import TESTING_PATH
from page_meta.models import MetaForPage, Meta

class TestMetaForPage(TestCase):

    def test_creation(self):
        meta = MetaForPage.objects.create(
            page_url='my-meta',
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        self.assertNotEqual(meta.pk, None)

    def test_get_default_meta(self):
        # default data is created by migration (example)
        default_meta = MetaForPage.get_default_meta()
        self.assertEqual(default_meta.page_url.lower(), 'default')

    def test_get_meta_from_url(self):
        # checking non existing meta
        current_meta = MetaForPage.get_meta_from_current_url()
        self.assertEqual(current_meta, None)

        # creating meta for current url
        MetaForPage.objects.create(
            page_url=TESTING_PATH,
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        current_meta = MetaForPage.get_meta_from_current_url()
        self.assertEqual(current_meta.page_url.lower(), TESTING_PATH.lower())

    def test_image_url(self):
        # testing if image_url contains full url
        meta = MetaForPage.objects.create(
            page_url='my-meta',
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        self.assertEqual(meta.image_url, 'http://localhost:8000/media/blog.jpg')

    def test_double_data_creation(self):
        # TODO:
        pass


class TestMeta(TestCase):
    def setUp(self):
        pass

    def test_initialization(self):
        _ = Meta(
            title='test title',
            description='test description',
            image_url='blog.jpg',
            keywords='test keywords'
        )

    def test_null_image(self):
        with self.assertRaises(ValueError):
            Meta(
                title='test title',
                description='test description',
                keywords='test keywords'
            )

    def test_image(self):
        # testing with model image
        meta = Meta(
            title='test title',
            description='test description',
            image=MetaForPage(image='blog.jpg').image
        )
        self.assertEqual(meta.image_url, 'http://localhost:8000/media/blog.jpg')

        # test with image path
        meta = Meta(
            title='test title',
            description='test description',
            image_url='http://localhost:8000/media/blog.jpg'
        )
        self.assertEqual(meta.image.url, 'http://localhost:8000/media/blog.jpg')


    def test_meta_for_pages_compatible(self):
        meta_for_page = MetaForPage(
            page_url='test',
            title='test title',
            description='test description',
            image='blog.jpg',
            keywords='test, keywords',
        )
        meta = Meta(
            title='test title',
            description='test description',
            image=MetaForPage(image='blog.jpg').image, # adding model image (ImageField)
            keywords='test, keywords',
        )
        
        # field comparison with MetaForPage and Meta
        self.assertEqual(meta_for_page.title, meta.title)
        self.assertEqual(meta_for_page.description, meta.description)
        self.assertEqual(meta_for_page.image, meta.image)
        self.assertEqual(meta_for_page.image.url, meta.image.url)
        self.assertEqual(meta_for_page.image_url, meta.image_url)
        self.assertEqual(meta_for_page.keywords, meta.keywords)


class TestMetaModelRender(TestCase):
    '''
    tests if the meta model renders correctly or not
    '''
    # TODO:
    pass