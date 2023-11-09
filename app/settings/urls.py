import api.webhooks as webhooks
from api.urls import well_known
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.sites import all_sites
from django.urls import include, path

urlpatterns = [
    path('api/v1/', include("api.urls")),
    *[path(f'{site.name}/', site.urls) for site in all_sites],
    path(".well-known/", include(well_known)),
    path('webhook/v1', webhooks.yookassaWebhookHandler),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
