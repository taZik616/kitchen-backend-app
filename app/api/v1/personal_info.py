from api.decorators import onlyCustomer
from api.models import Customer
from api.serializers import CustomerSerializer
from celery import shared_task
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@shared_task
def deleteAccountTask(customerId: int, deletionStartDate):
    customer = Customer.objects.filter(pk=customerId).first()
    if customer and customer.awaitingDeletion and customer.deletionStartDate == deletionStartDate:
        customer.user.is_active = False
        customer.user.save()


class CustomerPersonalInfoView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    parser_classes = [MultiPartParser]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

    @method_decorator(onlyCustomer)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # @method_decorator(onlyCustomer)
    # def put(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args)

    @method_decorator(onlyCustomer)
    def delete(self, request, *args, customer, **kwargs):
        customer.awaitingDeletion = True
        customer.deletionStartDate = timezone.now()
        customer.save()

        eta = timezone.now() + timezone.timedelta(days=30)
        deleteAccountTask.apply_async(
            [customer.pk, customer.deletionStartDate], eta=eta)
        return Response(status=204)


@api_view(['POST'])
@onlyCustomer
def cancelDeletionView(request, customer):
    customer.awaitingDeletion = False
    customer.deletionStartDate = None
    customer.save()

    return Response(status=200)
