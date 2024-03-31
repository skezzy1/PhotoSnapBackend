from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('api/user/', include('accounts.urls'))
=======
    path('api/user/', include('accounts.urls')), 
>>>>>>> origin/bugFix
    #path('home/', include(('home.urls','home'))),
]