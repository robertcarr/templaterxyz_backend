import shortuuid


def get_shortuuid(name=None, length=None):
    """ Return a short uuid, deterministic uuid or specific length random uuid """
    if not length:
        return shortuuid.uuid(name=name)
    else:
        return shortuuid.ShortUUID().random(length=length)

def get_upload_folder(instance, filename):
    """
    Return a string that is the upload folder/path without a leading or trailing '/'
    django.settings.MEDIA_ROOT is prepended to folder when saving

    If anonymous user (No Account) we will save it into a specific directory that holds all
    anon templates.  Otherwise, we should store it in folders based on account and repo

    :param instance: model instance
    :param filename: filename if available
    :return:  string of file path
    """
    if instance.user:
        return f"{instance.uuid}/{filename}"
    else:
        return f"_/{instance.uuid}/{filename}"


