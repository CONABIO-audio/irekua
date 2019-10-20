from thumbnails_irekua.thumbnails import register_processor


@register_processor('image/png')
@register_processor('image/jpeg')
def image_processor(item):
    print('YEAH')
