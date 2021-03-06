from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *

router = routers.SimpleRouter()


app_name = 'users'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/', CustomUserCreate.as_view(), name='create_user'),
    url(r'^update/', UpdateUserView.as_view(), name='update_user'),
    url(r'^all/', AllUsers.as_view(), name='list_users'),
    url(r'^retrieve/', RetrieveUser.as_view(), name='retrieve_user'),
    url(r'^delete/', AllUsers.as_view(), name='delete_user'),
    url(r'^login/', LoginView.as_view(), name='login_user'),
    url(r'^token/', RetrieveWithToken.as_view(),
        name='retrieve_with_token_user'),
]
