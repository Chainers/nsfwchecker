import http

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


class ImageNSFWRecognizerURLSerializer(serializers.Serializer):
    MAX_PHOTO_SIZE_IN_MB = settings.MAX_UPLOAD_SIZE / 1048576

    url = serializers.URLField()

    def validate_image(self, url):
        if not self.image_exists(url):
            msg = ('Size of the image is too big. Max size: {0} MB.'
                   .format(self.MAX_PHOTO_SIZE_IN_MB))
            raise serializers.ValidationError({'detail': [msg, ]})
        return url

    def image_exists_and_is_small(self, url):
        import urlparse
        parsed_url = urlparse.urlparse(url)
        domain = parsed_url.scheme + parsed_url.netloc
        path = parsed_url.path

        try:
            conn = http.client.HTTPConnection(domain)
            conn.request('HEAD', path)
            response = conn.getresponse()
            headers = response.getheaders()
            conn.close()
        except:
            return False

        try:
            length = int([x[1] for x in headers if x[0] == 'content-length'][0])
        except:
            length = 0
        if length > self.MAX_PHOTO_SIZE_IN_MB:
            return False

        return response.status == 200
