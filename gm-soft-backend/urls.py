"""gm-soft-backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from api.views import *

router = routers.SimpleRouter()
router.register(r'products', ProductsViewSet)
router.register(r'commands', CommandsViewSet)
router.register(r'commandRows', CommandRowsViewSet)
router.register(r'deliveries', DeliveriesViewSet)
router.register(r'deliveryDetails', DeliveryDetailsViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/user/', include('users.urls', namespace='users')),
    url(r'^api/token', token_obtain_pair),
    url(r'^api/token/refresh', token_refresh),
    url(r'^api/commandRow/command', getCommandRowByCommandId,
        name="commandRows of a commmand"),
    url(r'^api/deliveryDetail/delivery', getDeliveryDetailsByDeliveryId,
        name="delivery details by delivery id"),
    url(r'^api/product/quantity', getProductQuantityById,
        name="get product quantity by id")
]
