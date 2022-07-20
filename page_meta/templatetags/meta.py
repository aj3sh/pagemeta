from django import template
from django.contrib.auth.models import Group 

from page_meta.models import MetaForPage, Meta

register = template.Library() 

@register.simple_tag
def get_meta(context_meta=None):
    # meta from page url
    # HIGH PRIORITY
    meta = MetaForPage.get_meta_from_url()
    if meta:
        return meta

    # context meta
    if context_meta != None and (type(context_meta) == MetaForPage or type(context_meta) == Meta):
        return context_meta
    
    return MetaForPage.get_default_meta()