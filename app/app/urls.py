# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
else:
    urlpatterns = [
        path('secure-portal/', admin.site.urls)
    ]


urlpatterns += [
    path('api/secure/v1/', include('core.urls', namespace='core_v1')),
    path('api/secure/v2/', include('core.urls', namespace='core_v2')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Admin site settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
