COORDINATES_SCHEMA = {
    'type': 'dict',
    'keys': {
        'lat': {
            'type': 'number',
            'title': 'Широта',
            'required': True,
            'placeholder': '0.00000',
        },
        'long': {
            'type': 'number',
            'title': 'Долгота',
            'required': True,
            'placeholder': '0.00000',
        },
    }
}

ADDRESS_SCHEMA = {
    'type': 'dict',
    'keys': {
        'streetAndHouse': {
            'type': 'string',
            'title': 'Улица, дом',
            'required': True,
            'placeholder': 'пр Победы 228',
        },
        'entrance': {
            'type': 'string',
            'title': 'Подъезд',
            'required': False,
            'placeholder': '0',
        },
        'floor': {
            'type': 'string',
            'title': 'Этаж',
            'required': False,
            'placeholder': '0',
        },
        'flat': {
            'type': 'string',
            'title': 'Квартира',
            'required': False,
            'placeholder': '0',
        },
        'comment': {
            'type': 'string',
            'title': 'Комментарий',
            'required': False,
            'placeholder': '...',
        },
        'coordsLat': {
            'type': 'number',
            'title': 'Широта',
            'required': True,
            'placeholder': '0.00000',
        },
        'coordsLon': {
            'type': 'number',
            'title': 'Долгота',
            'required': True,
            'placeholder': '0.00000',
        },
    }
}
