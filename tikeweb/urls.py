"""tikeweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tikeshell import views as tikeshell_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',auth_views.login, {'template_name': 'html/login.html'}),
    url(r'^logout/$',auth_views.logout, {'next_page': '/login/'}),
    url(r'^$',tikeshell_views.home),
    url(r'^event/',tikeshell_views.event),
    url(r'^category/',tikeshell_views.category),
    url(r'^cart/',tikeshell_views.cart),
    url(r'^support/',tikeshell_views.support),
    url(r'^requestbuy/',tikeshell_views.requestbuy),
    url(r'^createacc/',tikeshell_views.createacc),
    url(r'^sitemap/',tikeshell_views.sitemap),
    url(r'^search/',tikeshell_views.search),
    url(r'^view_event/',tikeshell_views.view_event),
]
#urlpatterns=urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()