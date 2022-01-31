from django.conf.urls.static import static
from django.contrib import admin
# from django.template.defaulttags import url
from django.urls import path, include
# from django.views.static import serve

from UP import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tea_servise.urls')),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += staticfiles_urlpatterns()
