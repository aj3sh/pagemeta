from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import MetaForPage


@admin.register(MetaForPage)
class MetaForPageAdmin(admin.ModelAdmin):
    list_display = ("page_url", "title", "image_field", "image_resolution", "description", "keywords", "update", )
    fields = ("page_url", "title", "image", "description", "keywords",)
    search_fields = ("page_url", "title", )

    def update(self, obj):
        return format_html("""
            <a href="{}"
                style="padding: 8px 10px; background-color: #417690; border-radius: 5px; color: white; display: inline-block"
            >Update</a>
            <a href="{}"
                style="padding: 8px 10px; background-color: #ba2121; border-radius: 5px; color: white; display: inline-block"
            >Delete</a>
        """.format(
            reverse("admin:pagemeta_metaforpage_change", args=( obj.pk,)),
            reverse("admin:pagemeta_metaforpage_delete", args=( obj.pk,)),
        ))

    def image_field(self, obj):
        return format_html(f"""<a href="">
            <p>
                <img src="{obj.image.url}"
                     style="max-width: 150px; max-height: 150px; width: 100%; height: 100%" />
            </p>
            <p>{obj.image.name}</p>
        </a>""")

    def image_resolution(self, obj):
        return f"{obj.image_width} × {obj.image_height}"

MetaForPageAdmin.update.short_description = "Update"
MetaForPageAdmin.image_field.short_description = "Image"
MetaForPageAdmin.image_resolution.short_description = "Image Resolution"