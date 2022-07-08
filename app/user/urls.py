"""
URL mappings for the user API.
"""
from django.urls import path

from user.views import CreateUsersView


app_name = 'user'

urlpatterns = [
    path('user/create/', CreateUsersView.as_view(), name='create'),
]
