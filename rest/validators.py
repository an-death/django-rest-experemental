from django.utils.translation import gettext_lazy
from rest_framework.exceptions import ValidationError


###################################################################################
# DJANGO VALIDATORS
###################################################################################

class LowerCaseUnique(object):
    def __init__(self, type):
        self.type = type
        self.error_message = gettext_lazy('Duplicate values are not allow')

    def __call__(self, field_data, all_data):
        for t in globals()[self.type].effective.all():
            if field_data.lower() == t.name.lover():
                raise ValidationError(self.error_message)

###################################################################################
# DJANGO VALIDATORS END
###################################################################################
