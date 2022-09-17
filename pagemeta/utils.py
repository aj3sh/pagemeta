from django.apps import apps
from django.utils.module_loading import import_string


def get_meta(request, return_default=True):
    # importing models
    Meta = import_string('pagemeta.models.Meta')
    MetaForPage = apps.get_model('pagemeta.MetaForPage')
    
    # getting meta tag from url
    meta = MetaForPage.get_from_current_url()
    if meta:
        return Meta.from_meta_for_page(meta)

    # checking if any custom meta tag exists
    if hasattr(request, '_custom_meta') and request._custom_meta:
        return request._custom_meta

    if return_default:
        # checking and returning default meta tag
        default_meta = Meta.get_default()
        if default_meta:
            return default_meta

    # returning empty string
    return Meta.none()

def get_meta_exact(request):
    return get_meta(request, return_default=False)

def set_meta(request, meta):
    request._custom_meta = meta