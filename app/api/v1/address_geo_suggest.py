import json

import requests
from api.decorators import onlyCustomer
from api.models import Customer
from api.utils import getSetting
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view
from rest_framework.response import Response


@ratelimit(key='user_or_ip', rate='250/hour')
@api_view(['POST'])
@onlyCustomer
def addressGeoSuggestView(request, customer: Customer):
    try:
        setting = getSetting()
        if isinstance(setting, dict) and setting.get('error'):
            return Response(setting, status=400)

        streetAndHouse = request.data.get('streetAndHouse')

        resp = requests.get('https://suggest-maps.yandex.ru/v1/suggest', {
            'apikey': setting.map_suggest_api_key,
            'text': f'{customer.city.name}, {streetAndHouse}',
            'print_address': 1,
        }).json()

        data = resp.get('results')

        result = []

        if not data:
            return Response([])

        for item in data:
            street = None
            house = None

            for component in item.get("address", {}).get("component", []):
                if "STREET" in component.get("kind", []):
                    street = component["name"]
                elif "HOUSE" in component.get("kind", []):
                    house = component["name"]

            if street and house:
                address = item.get('address', {}).get('formatted_address', '')
                coordinates = {}
                # А яндекс молодцы, я не могу вернуть в сайджесте себе координаты и должен заюзать еще геокодер))
                resp = requests.get('https://geocode-maps.yandex.ru/1.x', {
                    'apikey': setting.map_geo_coder_api_key,
                    'geocode': address,
                    'format': 'json',
                }).json()

                point: str = resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                point = point.split(' ')
                coordinates = {
                    'lon': point[0],
                    'lat': point[1]
                }

                result.append({
                    'address': f"{street}, д. {house}",
                    'coordinates': coordinates
                })

        return Response(result)
    except Exception as e:
        print(e)
        return Response([])


@ratelimit(key='user_or_ip', rate='400/hour')
@api_view(['POST'])
@onlyCustomer
def addressByCoordsView(request, customer):
    try:
        setting = getSetting()
        if isinstance(setting, dict) and setting.get('error'):
            return Response(setting, status=400)

        long = request.data.get('long')
        lat = request.data.get('lat')

        if not long or not lat:
            return Response({'error': 'Необходимо указать координаты'}, status=400)

        resp = requests.get('https://geocode-maps.yandex.ru/1.x', {
            'apikey': setting.map_geo_coder_api_key,
            'geocode': f"{long},{lat}",
            'format': 'json',
        }).json()

        return Response({'address': resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']})
    except Exception as e:
        print(e)
        return Response([])
