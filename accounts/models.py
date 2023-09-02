from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	is_customer = models.BooleanField(default=False, help_text='Designate the user as a customer')
	is_collection_agent = models.BooleanField(default=False, help_text='Designate the user as a collection agent')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email


class CustomerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True, related_name='customerprofile')
	username = models.CharField(max_length=75, blank=True)
	first_name = models.CharField(max_length=75)
	last_name = models.CharField(max_length=75)
	other_name = models.CharField(max_length=75, blank=True)
	photo = models.ImageField(blank=True, upload_to='users/customers/%Y/%m/%d' )
	email = models.EmailField()
	email_confirmed = models.BooleanField(default=False)
	phone = PhoneNumberField()
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=75)
	location = models.CharField(max_length=75, blank=True)
	is_verified = models.BooleanField(default=False)
	updated_on = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return unicode(self.username)

	def __str__(self):
		return self.username
		
	# def get_absolute_url(self):
	# 	return reverse('accounts:shopper_profile', args=[str(self.id)])


class CollectionAgentProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='agentprofile')
	# agent_id = models.CharField(help_text='Unique ID for a merchant', max_length=25)
	first_name = models.CharField(max_length=75)
	last_name = models.CharField(max_length=75)
	other_name = models.CharField(max_length=75, blank=True)
	photo = models.ImageField(blank=True, upload_to='users/agents/%Y/%m/%d' )
	email = models.EmailField()
	email_confirmed = models.BooleanField(default=False)
	phone = PhoneNumberField()
	permanent_address = models.CharField(max_length=255)
	city = models.CharField(max_length=75)
	location = models.CharField(max_length=75, blank=True)
	about = models.TextField()
	date_of_birth = models.DateField(auto_now_add=True)
	is_verified = models.BooleanField(default=False)
	updated_on = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return unicode(self.username)

	def __str__(self):
		return self.email

	# def get_absolute_url(self):
	# 	return reverse('accounts:shopper_profile', args=[str(self.id)])
