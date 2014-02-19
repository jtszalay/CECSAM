from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from CECSAM.models import Location, Asset, Building
from CECSAM.forms import SearchForm
# Create your views here.
def index(request):
	#locations = Location.objects.all()
	#assets = Asset.objects.all()
	#context = {'locations':locations, 'assets':assets}
    	#return render(request, 'CECSAM/index.html', context)
	return HttpResponseRedirect(reverse('CECSAM.views.search'))

def test(request):
        context = {'next':request.path}
        return render(request, 'CECSAM/bulkScan.html', context)

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
		next = request.GET.get('next', '')
		return render(request, 'CECSAM/login.html', {'next': next})#return login page
		
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('CECSAM.views.index'))# Redirect to a success page.

def buildings(request):
        buildings = Building.objects.all()
        context = {'buildings':buildings, 'next':request.path}
        return render(request, 'CECSAM/buildings.html', context)

def building(request, building_short):
        building = get_object_or_404(Building, name=building_short)
	locations = Location.objects.filter(building__pk=building.pk)
        return render(request, 'CECSAM/building.html', {'building':building, 'locations':locations, 'next':request.path})

def locations(request):
        locations = Location.objects.all()
        context = {'locations':locations, 'next':request.path}
        return render(request, 'CECSAM/locations.html', context)

def location(request, location_id):
        location = get_object_or_404(Location, pk=location_id)
	assets = Asset.objects.filter(location__pk=location_id)
        return render(request, 'CECSAM/location.html', {'location':location, 'assets':assets, 'next':request.path})

def assets(request):
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
		context = {'assets':assets, 'next':request.path}
      		return render(request, 'CECSAM/assets.html', context)

def asset(request, asset_tag):
	c = {'next':request.path}
        c.update(csrf(request))
        locations = Location.objects.all()
	c['locations'] = locations
	try:
		asset = Asset.objects.get(tag=asset_tag)
	except:
		c['tag'] = asset_tag
		if not request.user.is_authenticated():
        		return redirect('/accounts/login/?next=%s' % request.path)
		else:
			return render(request, 'CECSAM/addAsset.html', c)
	c['asset'] = asset
	if request.method == 'POST': # If the form has been submitted...
		asset.location = Location.objects.get(id=request.POST['location'])
		asset.found = request.POST.get('found', False)
		asset.specifications = request.POST['specifications']
		if request.FILES.get('picture', False):
			asset.picture = request.FILES['picture']
		if request.POST.get('rmpicture', False):
			asset.picture = ""
		asset.save()
                return render(request, 'CECSAM/asset.html', c)
	else:
		return render(request, 'CECSAM/asset.html', c)

def search(request):
	c = {'next':request.path}
    	c.update(csrf(request))
	if request.method == 'POST': # If the form has been submitted...
            	return HttpResponseRedirect('/assets/'+request.POST['assetTag']) # Redirect after POST
    	else:
		return render(request, 'CECSAM/search.html', c)
