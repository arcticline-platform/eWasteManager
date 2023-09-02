import random

from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.tokens import account_activation_token
from accounts.models import User, CustomerProfile, CollectionAgentProfile
from agency.models import Agency


# General User Signup
class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = User
		fields = ('email', 'first_name', 'last_name',)

# General User Change Form
class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = User
		fields = ('email',)
		

# Signup for shoppers and creating their profiles
class CustomerSignUpForm(UserCreationForm):
	username = forms.CharField(max_length=30, widget=forms.TextInput(
			attrs={
				'placeholder': ' Choose your Username.'
			}),
			help_text='Must be unique.'
		)
	

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('email',)

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_shopper = True
		user.is_active = False
		user.is_staff = False
		user.is_superuser = False
		user.save()
		customer = CustomerProfile.objects.create(user=user)
		customer.username = self.cleaned_data.get('username')
		customer.email = self.cleaned_data.get('email')
		customer.save()
		return user

	# Validating the username to ensure it's unique
	def clean_username(self):
		username = self.cleaned_data['username']
		if CustomerProfile.objects.filter(username=username).exists():
			raise ValidationError('Username already taken. Please choose another one.')
		return username


# Customer Profile Edit Form
class CustomerProfileChangeForm(forms.ModelForm):

	class Meta:
		model = CustomerProfile
		fields = ('username','email', 'first_name', 'last_name', 'other_name', 'photo', 'phone', 'address', 'city', 'location')


# Forms for Collection Agents
class AgentSignUpForm(UserCreationForm):
	# agencyname = forms.CharField(max_length=30, widget=forms.TextInput(
	# 		attrs={
	# 			'placeholder': ' Choose your agencyname.'
	# 		}),
	# 		help_text='Must be unique to identify your business.'
	# 	)

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('email',)

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_trader = True
		user.is_active = False
		user.is_staff = False
		user.is_superuser = False
		user.save()
		# Creating agent Profile
		agent = CollectionAgentProfile.objects.create(user=user,)
		# agent.agencyname = self.cleaned_data.get('agencyname')
		agent.email = self.cleaned_data.get('email')
		agent.save()
		# Creating the Agency.
		agency = Agency.objects.create(agent=agent)
		agency.unique_id = self.generate_unique_id()
		agency.save()
		return user

	# Validating the agencyname to ensure it's unique
	# def clean_agencyname(self):
	# 	agencyname = self.cleaned_data['agencyname']
	# 	if Agency.objects.filter(agencyname=agencyname).exists():
	# 		raise ValidationError('agencyname already taken. Please choose another one.')
	# 	return agencyname

	# Generate Unique Ids
	def generate_unique_id(self):
		unique_id = Agency.unique_id
		alphabets = 'eWaste'
		numbers = '0123456789'
		alphanumeric = alphabets + numbers
		length = 9
		generate_id = "".join(random.sample(alphanumeric, length))
		if Agency.objects.filter(unique_id=unique_id).exists():
		    unique_id = "".join(random.sample(alphanumeric, length))
		    return unique_id
		else:
		    return generate_id

class CollectionAgentProfileChangeForm(forms.ModelForm):

	class Meta:
		model = CollectionAgentProfile
		fields = ('email', 'first_name', 'last_name', 'other_name', 'photo', 'phone', 'permanent_address', 'city', 'about', 'location')

