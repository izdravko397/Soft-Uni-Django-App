from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

def validate_published_date(value):
    if value > date.today():
        raise ValidationError(
            _('Published date cannot be in the future.'),
            params={'value': value},
        )


def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError(
            _('ISBN must be exactly 13 digits long.'),
            params={'value': value},
        )