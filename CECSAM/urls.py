from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf.urls import url, patterns, include
from CECSAM.models import Location, Building, Asset
from rest_framework import viewsets, routers

from django.contrib import admin

admin.autodiscover()

# ViewSets define the view behavior.
class AssetViewSet(viewsets.ModelViewSet):
    model = Asset

class LocationViewSet(viewsets.ModelViewSet):
    model = Location

class BuildingViewSet(viewsets.ModelViewSet):
    model = Building



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'buildings', BuildingViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'CECSAM.views.index', name='index'),
    url(r'^buildings/$', 'CECSAM.views.buildings', name='buidlings'),
    url(r'^buildings/(?P<building_short>[A-Z]+)/$', 'CECSAM.views.building', name='building'),
    url(r'^locations/$', 'CECSAM.views.locations', name='locations'),
    url(r'^locations/(?P<location_id>\d+)/$', 'CECSAM.views.location', name='location'),
    url(r'^locations/(?P<location_id>\d+)/bulkScan/$', 'CECSAM.views.bulkScan', name='bulkScan'),
    url(r'^assets/$', 'CECSAM.views.assets', name='assets'),
    url(r'^assets/(?P<asset_tag>[AaCc]\d+)/$', 'CECSAM.views.asset', name='asset'),
    url(r'^search/$', 'CECSAM.views.search', name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'CECSAM.views.login_view'),
    url(r'^accounts/logout/$', 'CECSAM.views.logout_view'),
    url(r'^api/csv/assets/$', 'CECSAM.api.assets_csv'),
    url(r'^api/csv/locations/(?P<location_id>\d+)/$', 'CECSAM.api.location_csv'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/rest/', include(router.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
