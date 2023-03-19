from django.urls import path
from .views import shoutouts, shoutouts_ready_to_read, update_shoutout

urlpatterns = [
    path('all/', shoutouts, name="get_all_shoutouts"),
    path('unread/', shoutouts_ready_to_read, name="unread_shoutout"),
    path('update/', update_shoutout, name="update_shoutout")

]
