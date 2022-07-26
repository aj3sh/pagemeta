from django.apps import apps
from django.utils.module_loading import import_string

def get_meta(request):
    # importing models
    Meta = import_string('pagemeta.models.Meta')
    MetaForPage = apps.get_model('pagemeta.MetaForPage')
    
    # getting meta tag from url
    meta = MetaForPage.get_meta_from_current_url()
    if meta:
        return Meta.from_meta_for_page(meta)

    # checking if any custom meta tag exists
    if hasattr(request, '_custom_meta') and request._custom_meta:
        return request._custom_meta

    # checking and returning default meta tag
    default_meta = Meta.from_meta_for_page(MetaForPage.get_default_meta())
    if default_meta:
        return default_meta

    # returning empty string
    return ''

def set_meta(request, meta):
    request._custom_meta = meta