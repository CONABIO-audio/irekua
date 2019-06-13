def view(user, annotation):
    if user.is_special:
        return True

    licence = annotation.item.licence
    licence_type = licence.licence_type

    if not licence.is_active:
        return True

    if licence_type.can_view_annotations:
        return True

    collection = annotation.item.collection
    collection_type = collection.collection_type

    if collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.has_user(user):
        return False

    return collection.has_permission(user, 'view_collection_annotations')


def create(user, item):
    if user.is_special:
        return True

    licence = item.licence
    licence_type = licence.licence_type

    # if not licence.is_active:
        # return True

    if licence_type.can_annotate:
        return True

    collection = item.collection
    collection_type = collection.collection_type

    if collection_type.is_admin(user):
        return True

    if collection.is_admin(user):
        return True

    if not collection.has_user(user):
        return False

    return collection.has_permission(user, 'add_collection_annotations')


def change(user, annotation):
    if user.is_superuser:
        return True

    if user.is_curator:
        return True

    collection = annotation.item.collection

    return annotation.created_by == user


def delete(user, annotation):
    if user.is_superuser:
        return True

    return annotation.created_by == user

