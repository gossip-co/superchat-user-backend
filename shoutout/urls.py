from django.urls import path
from .views import shoutouts

urlpatterns = [
    path('all/', shoutouts, name="get_all_shoutouts")
]
