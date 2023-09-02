from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from .forms import eWastePickUpForm, eWasteImageForm, AgencyProfileForm, CommentForm
from .models import Agency, eWaste, eWasteImages, Comments
from geopy.geocoders import Nominatim


def get_coordinates(address):
	geolocator = Nominatim(user_agent=user_agent)
	location = geolocator.geocode('address')
	full_address = location.address
	coordinates = (location.latitude, location.longitude)
	return JsonResponse(coordinates)


# Create your views here.
@login_required
def request_pick_up(request):
	if request.method == 'POST':
		form = eWastePickUpForm(request.POST)
		if form.is_valid():
			address = form.cleaned_data['address']
			geolocator = Nominatim(user_agent='JCS')
			location = geolocator.geocode(address)
			latitude = location.latitude
			longitude = location.longitude
			# print('#################### Cordinates ###########')
			# print(latitude, longitude)
			eWaste = form.save(commit=False)
			eWaste.location = Point(latitude, longitude)
			eWaste.client = request.user
			eWaste.save()
			messages.success(request, 'Pick Up Request Being Made...')
			return  HttpResponseRedirect('/agents/'+str(eWaste.id)+'/eWaste_Image/')
	else:
		form = eWastePickUpForm()
	return render(request, 'core/request_pick_up.html', {'form': form})

@login_required
def eWaste_details(request, id):
	ewaste = get_object_or_404(eWaste, id=id)
	images = eWasteImages.objects.filter(ewaste=ewaste).order_by('-uploaded')[:1]
	# print(images)
	comments = Comments.objects.filter(ewaste=ewaste).order_by('-created')[:1]

	return render(request, 'core/ewaste_details.html', {'ewaste':ewaste, 'images':images, 'comments': comments})

def eWaste_image(request, id):
	ewaste = get_object_or_404(eWaste, id=id)
	if request.method == 'POST':
		form = eWasteImageForm(request.POST or None, request.FILES)
		if form.is_valid():
			image = form.save(commit=False)
			image.ewaste = ewaste
			image.save()
			messages.success(request, 'eWaste Image Upload Successful! Request Submitted')
			return redirect('/')
	else:
		form = eWasteImageForm()
	return render(request, 'core/image_form.html', {'form': form, 'ewaste': ewaste})

def comment(request, id):
	ewaste = get_object_or_404(eWaste, id=id)
	if request.method == 'POST':
		form = CommentForm(request.POST or None, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.user = request.user
			comment.ewaste = ewaste
			comment.save()
			messages.success(request, 'eWaste comment Submitted Successful')
			return redirect('/')
	else:
		form = CommentForm()
	return render(request, 'core/comment_form.html', {'form': form, 'ewaste': ewaste})

def update_waste_status(request):
	ewasteId = request.POST.get('ewasteId')
	ewaste = eWaste.objects.get(id=ewasteId)
	ewaste.status = 'Picked'
	ewaste.save()
	return JsonResponse({'status': 'ok'})


def create_agency_profile(request, id):
	agency = get_object_or_404(Agency, id=id)
	pk = str(agency.agent.pk)
	if request.method == 'POST':
		form = AgencyProfileForm(request.POST, instance=agency)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/agency_admin/')
	else:
		form = AgencyProfileForm(instance=agency)
	return render(request, 'accounts/agents/admin/create_agency_profile.html', {'form': form})


def agency_list(request):
	agencies = Agency.objects.all()
	return render(request, 'core/agency_list.html', {'agencies': agencies})

def agency_details(request, id):
	agency = get_object_or_404(Agency, id=id)
	return render(request, 'core/agency_details.html', {'agency': agency})