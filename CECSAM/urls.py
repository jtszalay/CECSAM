from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CECSAM.views.index', name='index'),
    url(r'^api/buildings/$', 'CECSAM.views.buildings', {'api':True}),
    url(r'^api/buildings/(?P<building_short>[A-Z]+)/$', 'CECSAM.views.building', {'api':True}),
    url(r'^api/locations/$', 'CECSAM.views.locations', {'api':True}),
    url(r'^api/locations/(?P<location_id>\d+)/$', 'CECSAM.views.location', {'api':True}),
    url(r'^api/assets/$', 'CECSAM.views.assets', {'api':True}),
    url(r'^api/assets/(?P<asset_tag>[AC]\d+)/$', 'CECSAM.views.asset', {'api':True}),
    url(r'^buildings/$', 'CECSAM.views.buildings', name='buidlings'),
    url(r'^buildings/(?P<building_short>[A-Z]+)/$', 'CECSAM.views.building', name='building'),
    url(r'^locations/$', 'CECSAM.views.locations', name='locations'),
    url(r'^locations/(?P<location_id>\d+)/$', 'CECSAM.views.location', name='location'),
    url(r'^locations/(?P<location_id>\d+)/bulkScan/$', 'CECSAM.views.bulkScan', name='bulkScan'),
    url(r'^assets/$', 'CECSAM.views.assets', name='assets'),
    url(r'^assets/(?P<asset_tag>[AC]\d+)/$', 'CECSAM.views.asset', name='asset'),
    url(r'^search/$', 'CECSAM.views.search', name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'CECSAM.views.login_view'),
    url(r'^accounts/logout/$', 'CECSAM.views.logout_view'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
