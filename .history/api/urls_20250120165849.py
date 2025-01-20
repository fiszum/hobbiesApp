"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register', views.register, name='signup'),
    path('get-csrf-token', views.get_csrf_token, name='get_csrf_token'),
    path('currentuser/', views.current_user, name='current user'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', login_required(views.main_spa), name='main_spa'),
    path('sign-up/', views.register, name='sign_up'),
    path('top-users/', views.top_users, name='top_users'),
    path('updatehobbies/', views.update_hobbies, name="update_hobbies"),
    path('updateprofile/', views.update_profile, name='update_profile'),
    path('changepassword/', views.change_password, name='change_password'),
    path('send-friend-request/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/', views.accept_friend_request, name='accept_friend_request'),
    path('get-friend-requests/', views.get_friend_requests, name='get_friend_requests'),
    path('get-friends/', views.get_friends, name='get_friends'),
    path('all-hobbies/', views.get_all_hobbies, name='all_hobbies'),
    path('add_single_hobby/", views.add_single_hobby, name="add_single_hobby"),
     path('threads/', views.thread_list, name='thread_list'),

    re_path(r'^.*$', login_required(views.HobbiesSPA.as_view()), name='vue_app'),
]