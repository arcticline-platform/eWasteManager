from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import  HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, DetailView

from .models import User, CustomerProfile, CollectionAgentProfile
from accounts.tokens import account_activation_token, agent_account_activation
from .forms import CustomerSignUpForm, CustomerProfileChangeForm, AgentSignUpForm, CollectionAgentProfileChangeForm
from agency.models import Agency, eWaste

def homepage(request):
	context = {}
	return render(request, 'core/index.html', context)

class CustomerLogInView(LoginView):
	template_name = 'accounts/Login_Forms/customer_login.html'
	
	def get_success_url(self):
		url = self.get_redirect_url()
		return url or '/'


# Agent login view
class AgentLogInView(LoginView):
	template_name = 'accounts/Login_Forms/agent_login.html'
	
	def get_success_url(self):
		url = self.get_redirect_url()
		return url or '/accounts/agency_admin/'

# Sign up view
class SignUpView(TemplateView):
	template_name = 'registration/sign_up_view.html'


def customersignup(request):
	user_type = 'customer'
	if request.method == 'POST':
		form = CustomerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			domain_url = get_current_site(request)
			subject = 'Activate your Account on eWaste Manager'
			message = render_to_string('registration/account_activation_email.html', {
				'user': user,
				'domain': domain_url.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
				})
			user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = CustomerSignUpForm()
	return render(request, 'registration/signup_form.html', {'form':form, 'user_type':user_type})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, user.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.is_customer = True
		user.customerprofile.email_confirmed = True
		user.customerprofile.save()
		user.save()
		login(request, user)
		return redirect('/')


def account_activation_sent(request):
	return render(request, 'registration/account_activation_sent.html', {})


@login_required
def go_to_account(request):
	return render(request, 'accounts/myaccount.html', {})


@login_required
def customer_dashboard(request):
	user = request.user
	pick_up_requests = eWaste.objects.filter(client=user).order_by('-uploaded')
	return render(request, 'accounts/customers/customer_dashboard.html', {'user':user, 'pick_up_requests':pick_up_requests})


@login_required
def customerprofile(request, pk, template_name='accounts/customers/customer_account_profile.html'):
	customer_profile = get_object_or_404(CustomerProfile, pk=pk)
	return render(request, template_name, {'customer_profile':customer_profile})


@login_required
def customerProfileUpdate(request, pk, template_name='accounts/customers/profileeditform.html'):
	shopper = get_object_or_404(CustomerProfile, pk=pk)
	form = CustomerProfileChangeForm( request.POST or None, request.FILES, instance=customer)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/'+pk+'/shopperprofile/')
	return render(request, template_name, {'form':form})


@login_required
def customer_account_delete(request, pk,  template_name='accounts/account_delete.html'):
	customer_account = get_object_or_404(User, pk=pk)
	if request.method=='POST':
		customer_account.delete()
		return redirect('login')
	return render(request, template_name, {'object':customer_account})


# Views for Agents 
def agent_signup(request):
	user_type = 'agent'
	if request.method == 'POST':
		form = AgentSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			domain_url = get_current_site(request)
			subject = 'Activate your Agent Account on eWaste Manager'
			message = render_to_string('accounts/agents/account_activation_email.html',{
				'user': user,
				'domain': domain_url.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': agent_account_activation.make_token(user),
				})
			user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = AgentSignUpForm()
	return render(request, 'registration/signup_form.html', {'form':form, 'user_type':user_type })


def agent_account_activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, user.DoesNotExist):
		user = None
	if user is not None and agent_account_activation.check_token(user, token):
		user.is_active = True
		user.is_collection_agent = True
		user.agentprofile.email_confirmed = True
		user.agentprofile.save()
		user.save()
		login(request, user)
		return redirect('go_to_agent_account')

@login_required
def go_to_agent_account(request):
	return render(request, 'accounts/agents/go_to_agency_admin.html', {})

@login_required
def agency_admin(request):
	agent = request.user
	if agent.is_collection_agent:
		agent_profile = get_object_or_404(CollectionAgentProfile, user=agent)
		agency = get_object_or_404(Agency, agent=agent_profile)
		pick_up_requests = eWaste.objects.filter(agent=agency).order_by('-uploaded')
		return render(request, 'accounts/agents/admin/index.html', {'agent_profile': agent_profile, 'agency': agency, 'pick_up_requests': pick_up_requests})
	else:
		return redirect('agent_login')

@login_required
def agent_profile_view(request, pk, template_name='accounts/agents/admin/profile.html'):
	agent_profile = get_object_or_404(CollectionAgentProfile, pk=pk)
	agency = get_object_or_404(Agency, agent=agent_profile)
	pick_up_requests = eWaste.objects.filter(agent=agency)
	return render(request, template_name, {'agent_profile':agent_profile, 'agency': agency, 'pick_up_requests': pick_up_requests})

@login_required
def agent_profile_update(request, pk, template_name='accounts/agents/admin/profile_edit_form.html'):
	agent = get_object_or_404(CollectionAgentProfile, pk=pk)
	if request.method == 'POST':
		form = CollectionAgentProfileChangeForm(request.POST or None, request.FILES, instance=agent)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/'+pk+'/agent_profile/')
	else:
		form = CollectionAgentProfileChangeForm(instance=agent)
	return render(request, template_name, {'form':form, 'agent':agent})




















