from django.urls import path

from .views import user_registration

urlpatterns = [
    path('create/', user_registration, name="new_user_registration")
]
