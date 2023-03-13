from django.urls import path

from .views import test_payment, save_stripe_info, update_order_and_shoutout_status

urlpatterns = [
    path('test-payments/', test_payment, name="test-payment"),
    path('save-stripe-info/', save_stripe_info, name="save-stripe-info"),
    path('update-shoutout-order/<str:order_id>/<str:shoutout_id>/', update_order_and_shoutout_status)

]
