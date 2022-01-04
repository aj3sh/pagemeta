from django import template
from django.contrib.auth.models import Group 

from page_meta.models import MetaForPage, Meta

register = template.Library() 

@register.simple_tag
def get_meta(meta=None):
    if meta != None and (type(meta) == MetaForPage or type(meta) == Meta):
        return meta

    meta = MetaForPage.get_meta_from_url()
    if meta:
        return meta
    
    return MetaForPage.get_default_meta()