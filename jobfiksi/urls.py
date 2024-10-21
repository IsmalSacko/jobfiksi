"""
URL configuration for jobfiksi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from jobfiksi_api.views import (
    LoginView, LogoutView, 
    profileDetail, 
    UserCreateView, 
    AnnonceView, 
    AnnonceDetailView, 
    PostulerAnnonceView,
    home
    )





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobfiksi_api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/login/', include('rest_framework.urls', namespace='rest_framework')),
        # Route pour se connecter
     path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(('profile/restaurant/'), profileDetail, name='profile-detail'),
    path('users/', UserCreateView.as_view(), name='user_create'),
    path('annonces/', AnnonceView , name='annonce_create'),
    path('annonces/<int:pk>/', AnnonceDetailView.as_view(), name='annonce_detail'),
    path('annonces/<int:pk>/postuler/', PostulerAnnonceView.as_view(), name='postuler_annonce'),
    path('home/', home , name='home'),

   
  
  
]
