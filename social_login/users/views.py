import collections
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from users.forms import UserDetailsForm
from users.models import UserDetails
from users.models import SocialLoginDetails


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
            print("details and provider")

            if not SocialLoginDetails.objects.filter(user=user_obj, provider_social=provider):
                SocialLoginDetails.objects.create(user=user_obj, provider_social=provider, meta=meta_details)

            return render(request, 'home.html', {"has_password": True if user_obj.password else False })
        elif request.session.session_key:
            email = request.session['email']
            user = UserDetails.objects.get(email_field=email)
            return render(request, 'home.html', {'user_details': user, "has_password": True if user.password else False })
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

    base_url = reverse('home')
    request.session['email'] = email
    return redirect(base_url)


def all_user(request):
    users = UserDetails.objects.all()
    return render(request, 'all_users.html', {'user_details': users})


def single_user(request, user_id):
    users = get_object_or_404(UserDetails, id=user_id)
    return render(request, 'single_user.html', {'users': users})


def update_or_set_password(request):
    body = json.loads(request.body)
    email_field = body["email"]
    password_field = body["password"]
    UserDetails.objects.filter(email_field=email_field).update(password=password_field)
    return HttpResponse('Password updated successfully')


def update_phone(request):
    if request.method == 'PUT':
        body = json.loads(request.body)
        phone = body["phone"]
        email_field = body["email"]
        user_obj = UserDetails.objects.filter(email_field=email_field)
        if user_obj:
            UserDetails.objects.filter(email_field=email_field).update(phone=phone)
            return JsonResponse({'message': 'Phone updated successfully'}, status=200)
        return JsonResponse({'message': 'Error in Credentials'}, status=400)
    return render(request, 'update_phone.html')


def search_user(request, phone):
    users = get_object_or_404(UserDetails, phone=phone)
    return render(request, 'single_user.html', {'users': users})


def get_social_details(request, email):
    user = UserDetails.objects.get(email_field=email)
    social_login_details = SocialLoginDetails.objects.filter(user=user)
    print(social_login_details[0].user.email_field)
    return render(request, 'social_details.html', {'user_details': social_login_details})

