from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    path('materials/', include('materials.urls', namespace='materials')),
    path('users/', include('users.urls', namespace='users')),


]



