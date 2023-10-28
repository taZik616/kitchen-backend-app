from api.decorators import onlyCustomer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
@onlyCustomer
def myBonusesView(request, customer):
    return Response({'bonuses': customer.bonuses})
