from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


FREE_SCHEMA = _('free')
GENERIC_SAMPLING_EVENT = _('generic sampling event')
GENERIC_SITE = _('generic site')
GENERIC_COLLECTION = _('generic collection')


def validate_are_same_term_type(source, target):
    if source.term_type != target.term_type:
        msg = _('Term types must be equal for synonyms ({type1} != {type2})')
        msg = msg.format(
            type1=source.term_type,
            type2=target.term_type)
        raise ValidationError(msg)


def empty_json():
    return {}
