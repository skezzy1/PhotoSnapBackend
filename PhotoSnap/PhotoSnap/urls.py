from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/mainpage/', include('mainpage.urls'))
    #path('home/', include(('home.urls','home'))),
]