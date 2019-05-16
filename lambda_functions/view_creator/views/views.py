CREATORS = {}


class ViewCreator():
    @property
    def item_type(self):
        msg = 'Please determine the resulting item type of the view creator'
        raise NotImplementedError(msg)

    def __init__(self, item_file, database_info):
        self.item_file = item_file
        self.database_info = database_info

        self.create_view()

    def create_view(self):
        secondary_item = self.create_secondary_item()
        media_info = self.get_mediainfo()
        hash_string = hash_file(secondary_item)
        item_id = self.get_id()

        self.post_secondary_item(
            secondary_item=secondary_item,
            media_info=media_info,
            hash_string=hash_string,
            item_id=item_id)

    def create_secondary_item(self):
        pass

    def get_mediainfo(self):
        pass

    def get_id(self):
        pass

    def post_secondary_item(
            self,
            post_secondary_item=None,
            media_info=None,
            hash_string=None,
            item_id=None):
        pass


def create_view(item_file, database_info):
    item_type = item_file['item_type']

    try:
        creator_class = CREATORS[item_type]
        instance = creator_class(item_file, database_info)
        return instance
    except KeyError:
        msg = 'Quick view secondary item creator not implemented for {}'
        msg = msg.format(item_type)
        raise NotImplementedError(msg)


def register_creator(item_type):
    def decorator(klass):
        CREATORS[item_type] = klass
        return klass


def hash_file(item_file, block_size=65536):
    hasher = sha256()
    while True:
        data = item_file.read(block_size)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest()
