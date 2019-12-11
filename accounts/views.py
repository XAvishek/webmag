from django.shortcuts import render, redirect
from accounts.models import User
from django.views import View
from accounts.forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm, EmailSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
import json
import requests

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account succesfully created for {username}')
            login(request, user)
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                    instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'accounts/profile.html', context)

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'

def subscribe(email):
    data = {
        'email_address': email,
        'status': 'subscribed'
    }
    r = requests.post(
        members_endpoint,
        auth=('', MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()

def email_list_user(request):
    
    form = EmailSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email_user_qs = User.objects.filter(email=form.instance.email)
            if email_user_qs.exists():
                messages.info(request, 'You are already subscribed')
            else:
                subscribe(form.instance.email)
                form.save()
                messages.success(request, 'You have successfully subscribed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))