from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='homepage'),
    path('blogs/', views.BlogListView.as_view(), name='blogs-list'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blogs-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)