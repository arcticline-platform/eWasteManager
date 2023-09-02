from django.contrib import admin
from .models import Agency, eWaste, eWasteImages, Address, SubAddress, eWasteCategory
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
	list_display = ('unique_id', 'name','email', 'phone_number')
	list_per_page = 50
	serach_fields = ('name', 'email', 'description',)
	# list_filter = ('is_verified',)

class eWasteAdmin(OSMGeoAdmin):
	list_display = ('ewaste', 'address', 'client', 'agent', 'email', 'phone_contact')
	list_per_page = 50
	serach_fields = ('name', 'email', 'description', 'agent')
	list_filter = ('ewaste','status', 'agent', 'uploaded')


admin.site.register(Agency, AgencyAdmin)
admin.site.register(eWaste, eWasteAdmin)
admin.site.register(eWasteCategory)
admin.site.register(Address)
admin.site.register(SubAddress)
admin.site.register(eWasteImages)