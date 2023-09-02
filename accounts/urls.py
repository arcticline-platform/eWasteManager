from django.urls import include, path, re_path
from . import views


urlpatterns = [
	path('auths/', include('django.contrib.auth.urls')),
	

	# Logins
	path('customer/login/', views.CustomerLogInView.as_view(), name='customer_login'),
	path('agent/login/', views.AgentLogInView.as_view(), name='agent_login'),
	
	path('signup/', views.SignUpView.as_view(), name='signup_view'),

	# URLS for Customer Account
	path('customer/signup/', views.customersignup, name='customer_signup_view'),
	re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
	#activation 
	path('activate/<uidb64>/<token>', views.activate, name='activate'),
	path('go_to_account/', views.go_to_account, name='go_to_account'),
	path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
	path('<pk>/customerprofile/',  views.customerprofile, name='customer_profile'),
	path('int:<pk>/shopper_profile_update/', views.customerProfileUpdate, name='customer_profile_change'),
	# Account Delete
	path('int:<pk>/accountdelete/', views.customer_account_delete, name='customer_account_delete'),

	# URLS for Agent Account
	path('agent/signup/', views.agent_signup, name='agent_signup_view'),
	path('agent_account_activate/<uidb64>/<token>', views.agent_account_activate, name='agent_account_activate'),
	path('go_to_agent_account/', views.go_to_agent_account, name='go_to_agent_account'),
	path('agency_admin/', views.agency_admin, name='agency_admin'),
	path('<pk>/agent_profile/',  views.agent_profile_view, name='agent_profile_view'),
	path('int:<pk>/agent_profile_update/', views.agent_profile_update, name='agent_profile_update'),

]