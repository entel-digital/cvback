from storages.backends.gcloud import GoogleCloudStorage
from django.utils.deconstruct import deconstructible
from django.conf import settings


class StaticGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


@deconstructible
class MediaGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
    default_acl = None

    def __init__(self, *args, **kwargs):
        kwargs["bucket_name"] = getattr(settings, "PRIVATE_GS_BUCKET_NAME")
        kwargs["bucket_name"] = getattr(settings, "GS_EXPIRATION")
        super(MediaGoogleCloudStorage, self).__init__(*args, **kwargs)
