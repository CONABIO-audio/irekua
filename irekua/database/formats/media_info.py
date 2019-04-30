from .images import get_media_info as get_image_media_info


def get_media_info(tempfile):
    if 'image' in tempfile.content_type:
        get_image_media_info(tempfile)
    return {}
