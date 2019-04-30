import datetime
from .images import get_capture_date as get_image_capture_date


def get_capture_date(tempfile):
    if 'image' in tempfile.content_type:
        return get_image_capture_date(tempfile)

    return datetime.datetime.now()
