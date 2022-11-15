import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _, ngettext


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_contains_no_number',
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least 1 digit.",
            "Your password must contain at least 1 digits.",
            1,
        ) % {'min_length': 1}

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_contains_no_capital',
            )
    def get_help_text(self):
        return ngettext(
            "Your password must contain at least 1 uppercase letter.",
            "Your password must contain at least 1 uppercase letters.",
            1,
        ) % {'min_length': 1}
