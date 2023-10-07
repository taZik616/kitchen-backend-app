from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.sites import all_sites
from django.urls import path

urlpatterns = [
    *[path(f'{site.name}/', site.urls) for site in all_sites],
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

