from django.urls import include, path, re_path

from . import views

urlpatterns = [

	path('request_pick_up/', views.request_pick_up, name='request_pick_up'),
	path('<id>/eWaste_details/', views.eWaste_details, name='eWaste_details'),
	path('<id>/eWaste_Image/', views.eWaste_image, name='eWaste_image'),
	path('<id>/submit_comment/', views.comment, name='comment'),
	path('int<id>/create_agency_profile/', views.create_agency_profile, name='create_agency_profile'),
	path('agencies/', views.agency_list, name='agencies'),
	path('<id>/agency/', views.agency_details, name='agency_details'),
	path('ewaste_status_update/', views.update_waste_status, name='update_waste_status'),
]