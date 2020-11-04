from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')