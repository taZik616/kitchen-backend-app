from api.decorators import onlyCustomer
from api.models import Customer
from api.serializers import CustomerSerializer
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.is_active = False
        instance.user.save()
        return Response(status=204)
