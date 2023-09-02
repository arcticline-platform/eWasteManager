from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, CustomerProfile, CollectionAgentProfile


class UserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = UserAdmin
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_customer', 'is_collection_agent', 'is_active',)
	list_filter = ('is_staff','is_customer', 'is_collection_agent', 'is_active','date_joined', 'last_login',)
	add_fieldsets = (
			(None, {
				'classes': ('wide',),
				'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
				}
				),
		)
	list_per_page = 50
	fieldsets = (
			(None, {'fields': ('email','first_name', 'last_name', 'password', 'date_joined', 'last_login')}),
			('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
		)
	serach_fields = ('email', 'first_name', 'last_name',)
	ordering = ('email',)

class CustomerProfileAdmin(admin.ModelAdmin):
	list_display = ( 'user','email', 'username', 'first_name', 'last_name',)
	list_per_page = 50
	serach_fields = ('email', 'first_name', 'last_name',)
	list_filter = ('is_verified',)

class CollectionAgentProfileAdmin(admin.ModelAdmin):
	list_display = ( 'user','email', 'first_name', 'last_name',)
	list_per_page = 50
	serach_fields = ('email', 'first_name', 'last_name',)
	list_filter = ('is_verified',)


admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(CollectionAgentProfile, CollectionAgentProfileAdmin)