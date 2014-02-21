from django.contrib import admin
from CECSAM.models import Asset, Location, Building
# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    # ...
    list_display = ('tag', 'description', 'location', 'found', 'official', 'date')
    list_filter = ['date']
    search_fields = ['tag']

class BuildingAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name', 'longName')
    search_fields = ['name']

admin.site.register(Asset, AssetAdmin)
admin.site.register(Location)
admin.site.register(Building, BuildingAdmin)
