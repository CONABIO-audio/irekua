class Actions(object):
    LIST = 'list'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    METADATA = 'metadata'
    CREATE = 'create'
    DESTROY = 'destroy'
    RETRIEVE = 'retrieve'

    DEFAULT_ACTIONS = [
        LIST,
        UPDATE,
        PARTIAL_UPDATE,
        METADATA,
        CREATE,
        RETRIEVE,
        DESTROY,
    ]
