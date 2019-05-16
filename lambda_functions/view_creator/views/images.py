import io
from PIL import Image

from .views import ViewCreator, register_creator


@register_creator('image/png')
@register_creator('image/jpeg')
class ImageThumbnailCreator(ViewCreator):
    item_type = 'thumbnail'

    def create_secondary_item(self):
        image = Image.open(self.item_file)
        thumbnail = im.thumbnail((128, 128), Image.ANTIALIAS)

        secondary_item = io.BytesIO()
        thumbnail.save(secondary_item, format="JPEG")

        return secondary_item
