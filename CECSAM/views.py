from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.utils import simplejson

from CECSAM.models import Location, Asset, Building
from CECSAM.forms import SearchForm

def index(request):
	return HttpResponseRedirect(reverse('CECSAM.views.search'))

def login_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(request.POST['next'])# Redirect to a success page.
			else:
				pass# Return a 'disabled account' error message
		else:
			pass# Return an 'invalid login' error message.
	else:
		context= {'next': request.GET.get('next', '')}
		return render(request, 'CECSAM/login.html', context)#return login page
		
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('CECSAM.views.index'))# Redirect to a success page.

def buildings(request, api=False):
       	buildings = Building.objects.all()
	if api:
		return HttpResponse(simplejson.dumps({'buildings':list(buildings.values())}), mimetype='application/json')
	else:
	        context = {'buildings':buildings, 'next':request.path}
        	return render(request, 'CECSAM/buildings.html', context)

def building(request, building_short, api=False):
        building = get_object_or_404(Building, name=building_short)
	locations = Location.objects.filter(building__pk=building.pk)
	if api:
                return HttpResponse(simplejson.dumps({'building':Building.objects.filter(name=building_short).values()[0], 'locations':list(locations.values())}), mimetype='application/json')
        else:
		context = {'building':building, 'locations':locations, 'next':request.path}
        	return render(request, 'CECSAM/building.html', context)

def locations(request, api=False):
        locations = Location.objects.all()
	if api:
                return HttpResponse(simplejson.dumps({'buildings':list(locations.values())}), mimetype='application/json')
        else:
	        context = {'locations':locations, 'next':request.path}
	        return render(request, 'CECSAM/locations.html', context)

def location(request, location_id, api=False):
        location = get_object_or_404(Location, pk=location_id)
	assets = Asset.objects.filter(location__pk=location_id)
	if api:
                return HttpResponse(simplejson.dumps({'location':Location.objects.filter(pk=location_id).values()[0], 'assets':list(assets.values())}), mimetype='application/json')
        else:
		context = {'location':location, 'assets':assets, 'next':request.path}
	        return render(request, 'CECSAM/location.html', context)

def bulkScan(request, location_id):
	location = get_object_or_404(Location, pk=location_id)
        assets = Asset.objects.filter(location__pk=location_id)
        context = {'location':location, 'assets':assets, 'next':request.path}
        return render(request, 'CECSAM/bulkScan.html', context)

def assets(request, api=False):
	if request.method == "POST":
		asset = Asset()
		asset.tag = request.POST['tag']
		asset.description = request.POST['description']
		asset.model = request.POST['model']
		asset.serialId = request.POST['serialId']
		asset.location = Location.objects.get(id=request.POST['location'])
                asset.found = request.POST.get('found', False)
		asset.official = request.POST.get('official', False)
		asset.specifications = request.POST['specifications']
		asset.picture = request.FILES['picture']
                asset.save()
		return HttpResponseRedirect(reverse('CECSAM.views.asset', args=(asset.tag,))) 
	else:
		assets = Asset.objects.all()
		if api:
                	return HttpResponse(simplejson.dumps({'assets':list(assets.values('tag', 'description','found', 'official'))}), mimetype='application/json')
       		else:
			context = {'assets':assets, 'next':request.path}
      			return render(request, 'CECSAM/assets.html', context)

def asset(request, asset_tag, api=False):
	context = {'next':request.path}
        context.update(csrf(request))
        locations = Location.objects.all()
	context['locations'] = locations
	assets = Asset.objects.filter(tag=asset_tag)
	if len(assets) == 0 and not api:
		context['tag'] = asset_tag
		if not request.user.is_authenticated():
        		return redirect('/accounts/login/?next=%s' % request.path)
		else:
			return render(request, 'CECSAM/addAsset.html', context)
	elif request.method == 'POST': # If the form has been submitted...
		asset=assets[0]
		context['asset'] = asset
		asset.location = Location.objects.get(id=request.POST['location'])
		asset.found = request.POST.get('found', False)
		asset.specifications = request.POST['specifications']
		if request.FILES.get('picture', False):
			asset.picture = request.FILES['picture']
		if request.POST.get('rmpicture', False):
			asset.picture = ""
		asset.save()
                return render(request, 'CECSAM/asset.html', context)
	elif api:
		if len(assets) == 0:
			raise Http404
		else:
			return HttpResponse(simplejson.dumps({'assets':assets.values('tag', 'description','found', 'official')[0]}), mimetype='application/json')
	else:
		asset=assets[0]
		context['asset'] = asset
		return render(request, 'CECSAM/asset.html', context)

def search(request):
	context = {'next':request.path}
    	context.update(csrf(request))
	if request.method == 'POST': # If the form has been submitted...
            	return HttpResponseRedirect('/assets/'+request.POST['assetTag']) # Redirect after POST
    	else:
		return render(request, 'CECSAM/search.html', context)
