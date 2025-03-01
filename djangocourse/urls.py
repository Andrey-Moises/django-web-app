"""
URL configuration for djangocourse project.

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

from django.urls          import path, include
from django.contrib       import admin
from django.views.generic import RedirectView

from allauth.account.views import SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("app.urls")),
    #path("accounts/", include("django.contrib.auth.urls")), # Native Django authentication views | we include them all of them
    #path("", RedirectView.as_view(pattern_name="home")), # Redirect the user to the articles page
    path("", SignupView.as_view(), name="account_signup"), # Redirect the user to the articles page
    path("accounts/signup/", RedirectView.as_view(url="/")), # all auth views
    path("accounts/", include("allauth.urls")), # all auth views

    path("__debug__/", include("debug_toolbar.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
