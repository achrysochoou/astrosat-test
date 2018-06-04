"""astrosat URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from astrosat.views import *
from astrosat.views.services import *
from astrosat.views.api import *


# ALL OF THE (NON DJANGO-REST-FRAMEWORK) SERVICES..

service_urls = [
    # getting pending messages...
    path('messages/', get_django_messages, name="get_messages"),

    # ingesting new facilities...
    path('import_facilities/', import_facilities_now, name="import_facilities"),
]

# ALL OF THE DJANGO-REST-FRAMEWORK VIEWS...

api_urls = [
    re_path(r'^$', api_root),
    re_path(r'^facilities/$', FacilityViewSet.as_view({"get": "list"}), name="facilities-list"),
    re_path(r'^facilities/(?P<pk>[0-9]+)/$', FacilityViewSet.as_view({"get": "retrieve"}), name="facilities-detail"),
    re_path(r'^tasks/$', TaskResultViewSet.as_view({"get": "list"}), name="tasks-list"),
    re_path(r'^tasks/(?P<pk>[0-9]+)/$', TaskResultViewSet.as_view({"get": "retrieve"}), name="tasks-detail"),
]

admin.autodiscover()

# ERROR HANDLING...

handler404 = 'astrosat.views.page_not_found'
handler500 = 'astrosat.views.server_error'
handler403 = 'astrosat.views.permission_denied'
handler400 = 'astrosat.views.bad_request'

# PUTTING IT ALL TOGETHER...

urlpatterns = [

    # some low-level 3rd party templates have hard-coded the location of "favicon"; this pattern reroutes it correctly
    re_path(r'^favicon.ico$', serve, {
        'document_root': "{0}questionnaire/images/".format(settings.STATIC_ROOT),
        'path': 'favicon.ico',
    }),

    # admin...
    path('admin/', admin.site.urls),

    # authentication...
    path('accounts/', include('django.contrib.auth.urls')),

    # RESTful stuff...
    path('services/', include(service_urls)),
    path('api/', include(api_urls)),

    # the notes page (obviously)...
    path('notes/', notes, name="notes"),

    # a silly page for testing (obviously)...
    path('test/', test_view, name="test"),

    # the index page (obviosly)...
    path('', index, name="index"),

]
