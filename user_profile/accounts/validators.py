import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class SpecialCharacterValidator(object):
    """Custom password validator to ensure special characters are used in password."""
    def __init__(self, min_special=1):
        self.min_special = min_special

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}:;\[\]]"
        scan = [each for each in password if each in special_characters]
        if len(scan) < self.min_special:
            raise ValidationError(_('Password must contain at least {} special character.'.format(self.min_special)),)

    def get_help_text(self):
        return _('Password must contain at least {} special character.'.format(self.min_special))


class AlphaLowerCharacterValidator(object):
    """Custom password validator to ensure upper and lowercase characters are used."""
    def __init__(self, min_lower=1):
        self.min_lower = min_lower

    def validate(self, password, user=None):
        if len(re.findall(r"[a-z]", password)) < self.min_lower:
            raise ValidationError(_('Password must contain upper and lowercase characters.'),)

    def get_help_text(self):
        return _("Your password must contain at least {} lowercase character.".format(self.min_lower))

class AlphaUpperCharacterValidator(object):
    """Custom password validator to ensure upper and lowercase characters are used."""
    def __init__(self, min_upper=1):
        self.min_upper = min_upper

    def validate(self, password, user=None):
        if len(re.findall(r"[A-Z]", password)) < self.min_upper:
            raise ValidationError(_('Password must contain upper and lowercase characters.'),)

    def get_help_text(self):
        return _("Your password must contain at least {} uppercase character.".format(self.min_upper))

class NumericCharacterValidator(object):
    """Custom password validator to ensure at least a minimum number of digits are used."""
    def __init__(self, min_digs=1):
        self.min_digs = min_digs

    def validate(self, password, user=None):
        if len(re.findall(r'\d', password)) < self.min_digs:
            raise ValidationError(_('Password must contain at least {} digit.'.format(self.min_digs)),)

    def get_help_text(self):
        return _("Your password must contain at least 1 numeric character.")