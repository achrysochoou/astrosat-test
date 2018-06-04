"""astrosat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from astrosat.views import *
from astrosat.views.services import *
from astrosat.views.api import *


service_urls = [
    # getting pending messages...
    path('messages/', get_django_messages, name="get_messages"),

    # ingesting new facilities...
    path('import_facilities/', import_facilities_now, name="import_facilities"),
]

api_urls = [
    re_path(r'^$', api_root),
    re_path(r'^facilities/$', FacilityViewSet.as_view({"get": "list"}), name="facilities-list"),
    re_path(r'^facilities/(?P<pk>[0-9]+)/$', FacilityViewSet.as_view({"get": "retrieve"}), name="facilities-detail"),
    re_path(r'^tasks/$', TaskResultViewSet.as_view({"get": "list"}), name="tasks-list"),
    re_path(r'^tasks/(?P<pk>[0-9]+)/$', TaskResultViewSet.as_view({"get": "retrieve"}), name="tasks-detail"),
]

admin.autodiscover()

handler404 = 'astrosat.views.page_not_found'
handler500 = 'astrosat.views.server_error'
handler403 = 'astrosat.views.permission_denied'
handler400 = 'astrosat.views.bad_request'

urlpatterns = [

    # some low-level 3rd party templates have hard-coded the location of "favicon"; this pattern reroutes it correctly
    re_path(r'^favicon.ico$', serve, {
        'document_root': "{0}questionnaire/images/".format(settings.STATIC_ROOT),
        'path': 'favicon.ico',
    }),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('services/', include(service_urls)),
    path('api/', include(api_urls)),

    path('notes/', notes, name="notes"),

    path('test/', test_view, name="test"),

    path('', index, name="index"),

]
