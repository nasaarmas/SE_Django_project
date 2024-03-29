from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ValidationError

import re


class PasswordValidator:
    def __init__(self):
        self.regex = settings.PASSWORD_VALIDATION_REGEX

    def __call__(self, password, password_confirm, *args, **kwargs):
        if password is None or password_confirm is None:
            raise ValidationError({"password": [_('Please fill input fields')]})

        if password != password_confirm:
            raise ValidationError({"password": [_('Both password should be the same')]})

        if not re.search(self.regex, password):
            raise ValidationError({"password": [_('Password must be at least 8 character and contain symbols')]})

    def get_help_text(self):
        return (_(
            'Password must be at least 8 character and contain symbols'
        ))


validate_password = PasswordValidator()
