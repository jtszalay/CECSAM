import csv
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.template import loader, Context

from CECSAM.models import Location, Asset, Building

def location_csv(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    location.allFound = location.all_found()
    assets = Asset.objects.filter(location__pk=location_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+location.__unicode__()+'-assets.csv"'
    t = loader.get_template('api/assets.txt')
    c = Context({
        'data': assets,
    })
    response.write(t.render(c))
    return response

def assets_csv(request):
    assets = Asset.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'
    t = loader.get_template('api/assets.txt')
    c = Context({
        'data': assets,
    })
    response.write(t.render(c))
    return response
