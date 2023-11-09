from api.decorators import onlyCustomer
from api.models import CustomerAddress
from api.serializers import CustomerAddressCreateSerializer
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view
from rest_framework.response import Response


@ratelimit(key='user_or_ip', rate='100/hour')
@api_view(['PUT'])
@onlyCustomer
def addAddressView(request, customer):
    data = {
        'customer': customer.pk,
        'city': customer.city.pk,
        'streetAndHouse': request.data.get('streetAndHouse'),
        'entrance': request.data.get('entrance', ''),
        'floor': request.data.get('floor', ''),
        'flat': request.data.get('flat', ''),
        'comment': request.data.get('comment', ''),
        'coords': request.data.get('coords')
    }

    serializer = CustomerAddressCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    print(serializer.error_messages)
    print(serializer.errors)
    return Response({'error': 'Некорректные данные'}, status=400)


@ratelimit(key='user_or_ip', rate='100/hour')
@api_view(['PUT'])
@onlyCustomer
def changeAddressView(request, customer):
    id = request.data.get('id')

    customerAddress = CustomerAddress.objects.filter(
        customer=customer,
        city=customer.city,
        id=id,
    ).first()

    if customerAddress:
        data = {
            'customer': customer.pk,
            'city': customer.city.pk,
            'streetAndHouse': request.data.get('streetAndHouse'),
            'entrance': request.data.get('entrance', ''),
            'floor': request.data.get('floor', ''),
            'flat': request.data.get('flat', ''),
            'comment': request.data.get('comment', ''),
            'coords': request.data.get('coords')
        }
        serializer = CustomerAddressCreateSerializer(data=data)

        if serializer.is_valid():
            customerAddress.streetAndHouse = serializer.validated_data['streetAndHouse']
            customerAddress.entrance = serializer.validated_data['entrance']
            customerAddress.floor = serializer.validated_data['floor']
            customerAddress.flat = serializer.validated_data['flat']
            customerAddress.comment = serializer.validated_data['comment']

            customerAddress.save()

            return Response({'success': True, 'data': {**serializer.data, 'id': customerAddress.pk}})
        else:
            print(serializer.error_messages)
            print(serializer.errors)
            return Response({'error': 'Некорректные данные'}, status=400)

    return Response({'error': 'Не удалось найти адрес'}, status=400)


@ratelimit(key='user_or_ip', rate='150/hour')
@api_view(['DELETE'])
@onlyCustomer
def removeAddressView(request, customer):
    id = request.data.get('id')

    customerAddress = CustomerAddress.objects.filter(
        customer=customer,
        city=customer.city,
        id=id,
    ).first()

    customerAddress.delete()

    return Response({'success': 'Адрес был успешно удален'})


@ratelimit(key='user_or_ip', rate='150/hour')
@api_view(['POST'])
@onlyCustomer
def setDefaultAddressView(request, customer):
    id = request.data.get('id')
    if id == 0:
        customer.defaultAddress = None
        customer.save()
        return Response({'success': 'Адрес по умолчанию убран'})

    customerAddress = CustomerAddress.objects.filter(
        customer=customer,
        city=customer.city,
        id=id,
    ).first()

    customer.defaultAddress = customerAddress
    customer.save()

    return Response({'success': 'Этот адрес теперь по умолчанию'})
