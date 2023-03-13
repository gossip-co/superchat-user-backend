from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe

from .models import Orders
from shoutout.models import Shoutouts

stripe.api_key = "sk_test_51LsgyVSGPG8dWfbks7ckFLA2QWQ0sHMFiBRWwBLNmcccmDBN0S3e4AqdXtcboks2VsMqs0Qqasw5ktVmlnbqQo2F00FnwibGkt"
                  

@api_view(['POST'])
def test_payment(request):
    print("REXT PAYMENT >",request)
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='inr', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

# add try and error 
@api_view(['POST'])
def save_stripe_info(request):
    user = request.user
    data = request.data
    email = data['email']
    name = data['name']
    amount = data['amount']
    message = data['message']
    payment_method_id = data['payment_method_id']
    extra_msg  = ''

    print("DATA", data)
    
    # Checking if the customer with provided email is aleady exist or not
    customer_data = stripe.Customer.list(email=email).data
    # print("CUSTOMER DATA>>", customer_data)

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
      # creating customer
      customer = stripe.Customer.create(
      email=email, payment_method=payment_method_id, name=name)
    else:
      customer = customer_data[0]
      extra_msg = "Customer already existed."

    payment_in = stripe.PaymentIntent.create(
      customer=customer,
      payment_method=payment_method_id,
      currency='inr',
      amount=amount*100, #add rs to passa converter
      statement_descriptor="Superchat to carry ",
      confirm=True
      # meta_data :{
      #   name=
      # }
    )
    # print("PAYMENT INTENT", payment_in)
    client_secret = payment_in.client_secret

    if(payment_in.status=="requires_action"):
      shoutout_obj = Shoutouts.objects.create(
        user=user,
        message=message,
      )
      shoutout_obj.save()
      
      order_obj = Orders.objects.create(
        user=user,
        shoutout=shoutout_obj,
        amount=amount,
      )
      order_obj.save()
    return Response(status=status.HTTP_200_OK, 
      data={
        'message': 'Success', 
        'data': {'customer_id': customer.id, 'client_secret':client_secret, 'order_id': order_obj.id, 'shoutout_id': shoutout_obj.id,  'extra_msg': extra_msg}   }
    ) 

@api_view(['POST'])
def update_order_and_shoutout_status(request, order_id, shoutout_id):
  try:
    print("ORDER ID", order_id)
    print("Shout out id", shoutout_id)
    try:
      order_obj = Orders.objects.get(pk=order_id)
    except Exception as error:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      shoutout_obj = Shoutouts.objects.get(pk=shoutout_id)
    except ObjectDoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      order_obj.is_paid = True
      order_obj.save()
      shoutout_obj.is_published = True
      shoutout_obj.save()
    except Exception as error:
      return Response({"message": "Payment is reducted but shoutout is not posted, please contact the support"},status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "success"}, status=status.HTTP_200_OK)
    
  except Exception as error:
    return Response({"message": "Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

