from rest_framework.serializers import ValidationError


class ValidateLink:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = 'http://youtube.com'
        if value.get('link'):
            if link not in value.get('link'):
                raise ValidationError(f'Разрешена только ссылка на {link}')
        return None

