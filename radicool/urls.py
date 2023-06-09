"""
URL configuration for radicool project.

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
from django.urls import path, include
from django.conf import settings  # added to access local media
from django.conf.urls.static import static  # added to access local media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("allauth.urls")),
    path('', include("store.urls", namespace="store")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('checkout/', include("checkout.urls", namespace="checkout")),
    path('profile/', include("profiles.urls", namespace="profiles")),
]

if settings.DEBUG:  # uses local media while debug is true
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
