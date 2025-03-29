"""
URL configuration for schoolgid project.

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
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from blog.views import zvonki, search_users, school_map
from accounts.views import update_privacy

urlpatterns = [
    path('', RedirectView.as_view(url='/blog/')),
    path('admin/', admin.site.urls),
    path('profile/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('django.contrib.auth.urls')),
    path('bells_schedule/', zvonki, name='zvonki'),
    path('map/', school_map, name='map'),
    path('users_search/', search_users, name='search_users'),
    path('grades/', include('grades.urls')),
    path("update_privacy/", update_privacy, name="update_privacy"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)