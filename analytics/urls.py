"""analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps import insta

schema_view = get_schema_view(
    openapi.Info(
        title="Socan API",
        default_version="V1",
        description="SocAN",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('insta/', include('apps.insta.urls')),
                  path('user/', include('apps.users.urls')),
                  path('fb/', include('apps.fb.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    # Normal Schema UI
    url('api/v1/schema(?P<format>\.json|\.yaml)/$',schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Swagger Schema UI
    path('api/v1/swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger'),
    # path('api/internal/48751289/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    # ReDoc Schema UI
    path('api/v1/doc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]

admin.site.site_header = 'Hi Admin! Welcome to Socan'
admin.site.site_title = '[ Socan admin ]'
