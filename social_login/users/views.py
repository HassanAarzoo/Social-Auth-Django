import collections

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

from urllib.parse import urlencode

from django.contrib.sessions.models import Session
from users.forms import UserDetailsForm
from users.models import UserDetails
from users.models import SocialLoginDetails
from django.contrib.sessions.backends.db import SessionStore


def login(request):
    return render(request, 'login.html', {'form': UserDetailsForm()})


def home(request):
    if request.user and hasattr(request.user, 'is_authenticated'):
        user = request.user
        if isinstance(user.is_authenticated, collections.Callable):
            authenticated = user.is_authenticated()
        else:
            authenticated = user.is_authenticated
        if authenticated:

            for val in user.social_auth.values_list('provider'):
                provider = val[0]
            user_obj, created = UserDetails.objects.get_or_create(email_field=user.email)

            for data in user.social_auth.values_list('extra_data'):
                meta_details = data[0]
            if not SocialLoginDetails.objects.filter(user=user_obj, provider_social=provider):
                SocialLoginDetails.objects.create(user=user_obj, provider_social=provider, meta=meta_details)

            return render(request, 'home.html')
        elif request.session.session_key:
            email = request.session['email']
            user = UserDetails.objects.get(email_field=email)
            return render(request, 'home.html', {'user_details': user})
    return redirect(reverse('login'))


def validate_user(request):
    email = request.POST['email_field']
    name = request.POST['name']
    password = request.POST['password']

    if not UserDetails.objects.filter(email_field=email).exists():
        UserDetails.objects.create(name=name, email_field=email, password=password)
    else:
        user_obj = UserDetails.objects.get(email_field=email)
        if not user_obj.name:
            UserDetails.objects.filter(email_field=email).update(name=name)
        if password != user_obj.password:
            messages.error(request, 'Incorrect Password')
            return redirect('login')
        # TODO
        # This will be removed once edit option is put into html
        if not user_obj.password:
            UserDetails.objects.filter(email_field=email).update(password=password)

    base_url = reverse('home')
    request.session['email'] = email
    return redirect(base_url)


def all_user(request):
    users = UserDetails.objects.all()
    return render(request, 'all_users.html', {'user_details': users})


def single_user(request, user_id):
    users = get_object_or_404(UserDetails, id=user_id)
    return render(request, 'single_user.html', {'users': users})


def update_or_set_password(request, user_id):
    #TODO Get password from FE and set pass also check if it is a put request or not
    UserDetails.objects.filter(id=id).update()
    return HttpResponse('Password updated successfully')

# TODO Test this
def search_user(request, phone):
    users = get_object_or_404(UserDetails, id=phone)
    return render(request, 'single_user.html', {'users': users})