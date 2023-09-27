"""
URL configuration for users_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="User management",
        default_version='v1',
        description="Ce projet est une application web qui permet la gestion des utilisateurs avec des opérations CRUD (Create, Read, Update, Delete) ainsi que les fonctionnalités de login, registration (inscription), et forgot password (mot de passe oublié) en utilisant Django Rest Framework (DRF)",
        terms_of_service="",
        contact=openapi.Contact(email="alphonse.danni@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]
