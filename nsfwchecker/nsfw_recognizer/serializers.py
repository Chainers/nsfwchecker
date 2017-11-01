from django.conf import settings
from rest_framework import serializers


class ImageNSFWRecognizerSerializer(serializers.Serializer):

    MAX_PHOTO_SIZE_IN_MB = settings.MAX_UPLOAD_SIZE / 1048576

    image = serializers.ImageField()

    def validate_image(self, image):
        # TODO: add check that file is actually an image
        # (e.g. using libmagic, this could be moved
        # into common utility method)
        if image.size > settings.MAX_UPLOAD_SIZE:
            msg = ('Size of the uploaded file is too big. Max size: {0} MB.'
                   .format(self.MAX_PHOTO_SIZE_IN_MB))
            raise serializers.ValidationError({'detail': [msg, ]})
        return image
