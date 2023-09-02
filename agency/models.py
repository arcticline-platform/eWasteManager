from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from accounts.models import User, CustomerProfile, CollectionAgentProfile


class Address(models.Model):
	place_name = models.CharField(max_length=75)
	coordinates = models.PointField(blank=True, srid=4326, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.place_name

	class Meta:
		verbose_name = 'Address'
		verbose_name_plural = 'Addresses'


class SubAddress(models.Model):
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	place_name = models.CharField(max_length=75)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.place_name

	class Meta:
		verbose_name = 'Sub Address'
		verbose_name_plural = 'Sub Addresses'


# Create your models here.
class Agency(models.Model):
	agent = models.ForeignKey(CollectionAgentProfile, on_delete=models.CASCADE, related_name='agents')
	name = models.CharField(max_length=75, verbose_name='Agency Name', help_text='Name of Collection Agency')
	unique_id = models.CharField(max_length=11)
	description = RichTextField(verbose_name='Decribe your Agency')
	phone_number = PhoneNumberField(help_text='Agencys Phone Number', verbose_name='Agency Phone Number')
	email = models.EmailField(max_length=75, verbose_name='Agency Email')
	location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
	price = models.CharField(blank=True, max_length=75, help_text="Set your Pricing for Unit Items e.g 1000/= per Kg")
	tranport_fee = models.CharField(blank=True, max_length=75, help_text="Set your Transport Fee for Unit Items e.g 1000/= per Km")
	logo = models.ImageField(verbose_name='Agency logo', upload_to='Images/Agency/logos')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = _('Agency')
		verbose_name_plural = _('Agencies')

	def __str__(self):
		return self.name


class eWasteCategory(models.Model):
	name = models.CharField(max_length=75)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'eWaste Category'
		verbose_name_plural = 'eWaste Categories'


class eWaste(models.Model):
	STATUS = (
		('picked', 'Picked'),
		('pending', 'Pending'),
	)
	# name = models.CharField(max_length=75, verbose_name='Item Name', help_text="Item's name")
	ewaste = models.ForeignKey(eWasteCategory, on_delete=models.CASCADE, verbose_name='Select eWaste', help_text='Select the eWaste you want to upload')
	address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name= "City Division", help_text='Please select your Division')
	sub_address = models.ForeignKey(SubAddress, on_delete=models.CASCADE, verbose_name= "Address in Division", help_text='Please select the location of the Item', null=True, blank=True)
	client = models.ForeignKey(User, on_delete=models.CASCADE)
	agent = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, verbose_name='Collection Agent', help_text='Choose an Agent to Pick Up your Item')
	description = RichTextField(verbose_name=_("Item Description"), help_text=_("Describe your Item."))
	quantity = models.PositiveIntegerField(validators=[MaxValueValidator(1000)], verbose_name='Quantity', help_text='Weight in Kilos')
	phone_contact = PhoneNumberField(verbose_name='Contact Phone', help_text='Phone Number to link up for the Item')
	email = models.EmailField(max_length=75, verbose_name='Contact Email', help_text='Email linked to link up for the Item')
	status = models.CharField(max_length=25, choices=STATUS, default='Pending', help_text=_('Designate if the the item was picked or not'))
	uploaded = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name = _('eWaste')

	def __str__(self):
		return self.email


class eWasteImages(models.Model):
	ewaste = models.ForeignKey(eWaste, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='Images/eWaste', verbose_name='eWaste Image', help_text='upload an Image for the eWaste')
	uploaded = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'eWaste Image'
		verbose_name_plural = 'eWaste Images'

	# def __str__(self):
	# 	return self.


class Comments(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ewaste = models.ForeignKey(eWaste, on_delete=models.CASCADE)
	comment = RichTextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)