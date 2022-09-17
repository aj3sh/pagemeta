from unittest.mock import patch

from django.http import HttpRequest
from django.test import TestCase

from pagemeta.models import MetaForPage, Meta

def get_fake_request():
    '''returns fake request (used for testing purpose only)'''
    request = HttpRequest()
    request.META['SERVER_NAME'] = 'localhost'
    request.META['SERVER_PORT'] = '8000'
    request.path = '/test'
    return request

class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        
        # mocking pagemeta.models.get_request with get_fake_request
        self.request_patcher = patch('pagemeta.models.get_request')
        self.mock_get_request = self.request_patcher.start()
        self.mock_get_request.return_value = get_fake_request()

        # mocking pagemeta.requests.get_request with get_fake_request
        self.request_patcher2 = patch('pagemeta.requests.get_request')
        self.mock_get_request2 = self.request_patcher2.start()
        self.mock_get_request2.return_value = get_fake_request()

    def tearDown(self):
        self.request_patcher.stop()
        self.request_patcher2.stop()
        super().tearDown()

class TestMetaForPage(BaseTestCase):

    def test_creation(self):
        meta = MetaForPage.objects.create(
            page_url='my-meta',
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        self.assertNotEqual(meta.pk, None)

    def test_get_default(self):
        # default data is created by migration (pagemeta_example)
        default_meta = MetaForPage.get_default()
        self.assertEqual(default_meta.page_url.lower(), 'default')

    def test_get_meta_from_url(self):
        # checking non existing meta
        current_meta = MetaForPage.get_from_current_url()
        self.assertEqual(current_meta, None)

        # creating meta for current url
        request = get_fake_request()
        MetaForPage.objects.create(
            page_url=request.path,
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        current_meta = MetaForPage.get_from_current_url()
        self.assertEqual(current_meta.page_url.lower(), request.path.lower())

    def test_double_data_creation(self):
        # TODO:
        pass


class TestMeta(BaseTestCase):

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
        self.assertEqual(meta_for_page.keywords, meta.keywords)

    def test_meta_for_pages_conversion(self):
        # testing if image_url contains full url
        meta_for_page = MetaForPage.objects.create(
            page_url='my-meta',
            title='Test title',
            image='blog.jpg',
            description='test description',
            keywords='test,keywords',
        )
        meta = Meta.from_meta_for_page(meta_for_page)
        self.assertEqual(meta.title, meta_for_page.title)
        self.assertEqual(meta.description, meta_for_page.description)
        self.assertEqual(meta.image, meta_for_page.image)
        self.assertEqual(meta.description, meta_for_page.description)
        self.assertEqual(meta.image_url, 'http://localhost:8000/media/blog.jpg')

    def test_meta_default(self):
        self.assertEqual(Meta.get_default().title, MetaForPage.get_default().title)

    def test_none_meta(self):
        self.assertEqual(str(Meta.none()), '')
        self.assertEqual(bool(Meta.none()), False)

class TestMetaModelRender(BaseTestCase):
    '''
    tests if the meta model renders correctly or not
    '''
    
    def setUp(self):
        super().setUp()
        self.meta = Meta(
            title='test title',
            description='test description',
            image_url='http://localhost:8000/media/blog.jpg'
        )

    def test_meta_tag_rendering(self):
        self.assertTrue('<link rel="canonical" href="http://localhost:8000/test" />' in str(self.meta))
        self.assertTrue('<meta name="title" content="test title" />' in str(self.meta))
        self.assertTrue('<meta name="description" content="test description" />' in str(self.meta))

    def test_og_rendering(self):
        self.assertTrue('<meta property="og:title" content="test title" />' in str(self.meta))
        self.assertTrue('<meta property="og:description" content="test description" />' in str(self.meta))
        self.assertTrue('<meta property="og:url" content="http://localhost:8000/test" />' in str(self.meta))
        self.assertTrue('<meta property="og:image" content="http://localhost:8000/media/blog.jpg" />' in str(self.meta))

    def test_twitter_card_rendering(self):
        self.assertTrue('<meta name="twitter:title" content="test title" />' in str(self.meta))
        self.assertTrue('<meta name="twitter:description" content="test description" />' in str(self.meta))
        self.assertTrue('<meta name="twitter:image" content="http://localhost:8000/media/blog.jpg" />' in str(self.meta))
