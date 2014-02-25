from django.db import models

def asset_url_builder(instance, filename):
    return 'assets/'+instance.tag+"/"+filename

# Create your models here.
class Asset(models.Model):
    tag = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255)
    location = models.ForeignKey('Location')
    serialId = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    found = models.BooleanField()
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    official = models.BooleanField()    
    specifications = models.TextField()
    picture = models.ImageField(upload_to=asset_url_builder)    

    ordering = ['location'] 

    def __unicode__(self):
        return self.tag + ' ' + self.description

class Location(models.Model):
    building = models.ForeignKey('Building')
    room = models.CharField(max_length=20)

    ordering = ['-building', 'room']
    unique_together = ("building", "room")

    def __unicode__(self):
        return self.building.__unicode__() + ' ' + self.room

    def all_found(self):
        return all([a.found for a in Asset.objects.filter(location__id=self.id)])

class Building(models.Model):
    name = models.CharField(max_length=20)
    longName = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    def all_found(self):
        return all([l.all_found() for l in Location.objects.filter(building__pk=self.pk)])
