"""budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from rest_framework import routers
from rest_framework_nested import routers

from api.views import (IncomeViewSet,
                       NestedCategoryViewSet,
                       CategoryViewSet,
                       NestedWasteViewSet)

routes = routers.SimpleRouter()
routes.register('incomes', IncomeViewSet)
routes.register(r'categories', CategoryViewSet)

incomes_routes = routers.NestedSimpleRouter(routes, r'incomes', lookup='income')
incomes_routes.register(r'categories', NestedCategoryViewSet)

waste_routes = routers.NestedDefaultRouter(incomes_routes, r'categories', lookup='cat')
waste_routes.register(r'wastes', NestedWasteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(routes.urls)),
    path('api/v1/', include(incomes_routes.urls)),
    path('api/v1/', include(waste_routes.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
