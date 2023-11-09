from uuid import uuid4

import requests
from api.constants import PAYMENT_METHODS_ARRAY
from api.decorators import onlyCustomer
from api.models import (
    Customer,
    CustomerAddress,
    Order,
    OrderProduct,
    Product,
    ProductInfoInCity,
)
from api.utils import getSetting
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
@onlyCustomer
def makeOrderView(request, customer: Customer):
    products = request.data.get('products')
    paymentMethod = request.data.get('paymentMethod')
    useBonuses = request.data.get('useBonuses')
    address = request.data.get('addressId')

    setting = getSetting()
    if isinstance(setting, dict) and setting.get('error'):
        return Response(setting, status=400)

    if paymentMethod not in PAYMENT_METHODS_ARRAY:
        return Response({'error': 'Укажите метод оплаты'}, status=400)

    address = CustomerAddress.objects.filter(
        hasBeenDeleted=False, pk=address).first()
    if not address:
        return Response({'error': 'Укажите правильный адрес'}, status=400)

    resp = {
        'total': 0,
    }
    order = Order.objects.create(
        customer=customer,
        city=customer.city,
        paymentMethod=paymentMethod,
        useBonuses=useBonuses,
        address={
            'coordsLat': address.coords['lat'],
            'coordsLon': address.coords['long'],
            'streetAndHouse': address.streetAndHouse,
            'entrance': address.entrance,
            'floor': address.floor,
            'flat': address.flat,
            'comment': address.comment,
        }
    )
    for prod in products:
        id = prod['id']
        quantity = int(prod['quantity'])
        if quantity <= 0:
            return Response({'error': 'Кол-во товара должно быть положительным'}, status=400)

        product = Product.objects.filter(pk=id).first()
        productInfo = ProductInfoInCity.objects.filter(
            product=product, city=customer.city).first()
        if product:
            OrderProduct.objects.create(
                product=product,
                productInfo=productInfo,
                quantity=quantity,
                order=order,
            )

            productsPrice = productInfo.price * quantity
            resp['total'] = resp['total'] + productsPrice
        else:
            return Response({'error': 'Некоторые товары не были найдены'}, status=400)

    if useBonuses:
        discount = min(int(customer.bonuses), resp['total'])
        resp['total'] -= min(int(customer.bonuses), resp['total'])
        customer.bonuses -= discount

    if paymentMethod == 'online':
        auth = (setting.yookassa['shopId'], setting.yookassa['secretKey']) if not setting.useTest else (
            setting.test_yookassa['shopId'], setting.test_yookassa['secretKey'])
        response = requests.post(
            'https://api.yookassa.ru/v3/payments', headers={
                'Idempotence-Key': str(uuid4()),
                'Content-Type': 'application/json',
            }, json={
                'amount': {
                    # f"{orderData['total']:.2f}", - если Decimal
                    'value': f"{int(resp['total'])}.00",
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'embedded',
                },
                # 'save_payment_method': True, # Нельзя, нужно связаться с поддержкой для подключения
                'capture': True,  # Если False то деньги замораживаются
                'description': f'Покупка баланса внутри системы приложения Kitchen',
                'merchant_customer_id': customer.user.username,
                'metadata': {
                    'product': 'inAppBalance',
                    'orderNumber': order.pk,
                    'sumToBuy': int(resp['total']),
                    'bonuses': int(customer.bonuses)
                },
            }, auth=auth)
        paymentResponse = response.json()

        if paymentResponse.get('type') == 'error':
            order.delete()
            return Response({'error': 'Не удалось создать страницу с оплатой'}, status=400)

        confirmation = paymentResponse['confirmation']
        confirmationType = confirmation['type']
        confirmationToken = confirmation['confirmation_token']
        customer.save()
        if confirmationToken:
            order.confirmationToken = confirmationToken
            order.save()
            return Response({
                'success': True,
                'confirmationToken': confirmationToken,
                'confirmationType': confirmationType,
                **resp
            })
        else:
            order.delete()
            return Response({'error': 'Не удалось вернуть токен для оплаты'})

    customer.save()
    return Response({'success': 'Заказ создан', **resp})
