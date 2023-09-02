from django import forms
from django.db import transaction
from django.forms import ModelForm

from .models import Agency, eWaste, eWasteImages, Comments

# Customer Profile Edit Form
class eWastePickUpForm(forms.ModelForm):

	class Meta:
		model = eWaste
		fields = ('agent','ewaste', 'address', 'sub_address', 'description', 'quantity', 'phone_contact', 'email')


class eWasteImageForm(forms.ModelForm):

	class Meta:
		model = eWasteImages
		fields = ('image',)


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ('comment',)


class AgencyProfileForm(forms.ModelForm):

	class Meta:
		model = Agency
		fields = ('name', 'description', 'phone_number', 'email', 'location', 'price', 'tranport_fee')