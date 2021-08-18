from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()


app_name = 'users'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/', CustomUserCreate.as_view(), name='create_user'),
    url(r'^update/', UpdateUserView.as_view(), name='update_user'),
    url(r'^all/', AllUsers.as_view(), name='list_users'),
    url(r'^retrieve/', RetrieveUser.as_view(), name='retrieve_user'),
    url(r'^logout/blacklist', BlackListTokenView.as_view(), name='logout_user'),
    url(r'^login/', LoginUser.as_view(), name='login_user'),
]