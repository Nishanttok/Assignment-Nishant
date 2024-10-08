"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from basics import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

swagger_info = openapi.Info(
		title="Backend Api",
		default_version='v1',
		description="Online",
		contact=openapi.Contact(email="contact@nishant.com"),
	)
schema_view = get_schema_view(
    validators=['ssv', 'flex'],
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ApiIndexView(request):
	return HttpResponse("<h1>Welcome to Backend APIs, Developed by Nishant. </h1>")
urlpatterns = [
	path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	path('', ApiIndexView,name="initial_page"),
	path('django-admin/', admin.site.urls),
	path('project/account/', include('account.urls')),
	path('project/product_management/', include('product_management.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
