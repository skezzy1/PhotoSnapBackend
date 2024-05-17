from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="PhotoSnap API",
        default_version='v1',
        description="API documentation for PhotoSnap",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@photosnap.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('APIschema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/mainpage/', include('mainpage.urls'))
    #path('home/', include(('home.urls','home'))),
]