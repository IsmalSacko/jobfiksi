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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from jobfiksi_api.views import login_view, profile_view, register_view, UserTypeList




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobfiksi_api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('api/user-types/', UserTypeList.as_view(), name='user-types'),
  
  
]
