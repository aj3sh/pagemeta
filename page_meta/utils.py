from django.apps import apps

def get_meta(request):
    MetaForPage = apps.get_model('page_meta.MetaForPage')
    # return MetaForPage.get_meta_from_current_url()
    return MetaForPage.get_default_meta()

def set_meta(request, meta):
    request._custom_meta = meta