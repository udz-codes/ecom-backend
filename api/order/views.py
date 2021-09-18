from django.contrib.auth.backends import UserModel
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from .serializers import OrderSerializer


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({
            'error':'Please re-login',
            'code': '1'
        })

    if request.method == "POST":
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']
        address = request.POST['address']
        phone = request.POST['phone']

        total_prod = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return JsonResponse({
                'error':'User does not exist'
            })

        order = Order(
            user=user,
            product_names=products,
            total_products=total_prod,
            total_amount=amount,
            address=address,
            phone=phone,
            email=user.email
        )

        order.save()

        return JsonResponse({
            'success': True,
            'error': False,
            'msg': 'Order placed succesfully'
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer