from PIL import Image
from PIL.ExifTags import TAGS


def get_exif(fn):
    ret = {}
    image = Image.open(fn)
    info = image._getexif()

    if info is None:
        return ret

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def get_media_info(tempfile):
    media_info = {}

    exif = get_exif(tempfile)
    media_info.update(exif)
    return media_info


def get_capture_date(tempfile):
    exif = get_exif(tempfile)
    try:
        return exif["DateTime"]
    except KeyError:
        raise IOError("No date was found in image file")
