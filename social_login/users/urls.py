from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('validate_user', views.validate_user, name='validate_user'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('all_users/', views.all_user, name='user'),
    path('single_user/<int:user_id>/', views.single_user, name='single_user'),
    path('update_pass/', views.update_or_set_password, name='update_or_set_password'),
    path('search_user/<str:phone>', views.search_user, name='search_user')
]
