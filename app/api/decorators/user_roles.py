from api.models import Customer
from rest_framework.response import Response


def onlyCustomer(view_func):
    '''
    Функция вызывает представление с параметрами: `(request, customer, *args, **kwargs)`, если объект нужной модели найден
    '''
    def wrapped(request, *args, **kwargs):
        errorResp = Response(
            {"error": "Это действие разрешено только покупателям"},
            status=400,
        )
        user = request.user
        try:
            if user.is_authenticated:
                customer = Customer.objects.get(user=user)
                return view_func(request, *args, customer=customer, **kwargs)
            else:
                return errorResp
        except Customer.DoesNotExist:
            return errorResp
    return wrapped
