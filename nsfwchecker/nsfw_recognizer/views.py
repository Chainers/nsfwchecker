import urllib
import logging
import os
import requests
from io import StringIO
from PIL import Image

from rest_framework import (
    generics,
    parsers,
    permissions,
    response,
)

from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from .classifier import NSFWImageClassifier
from .serializers import ImageNSFWRecognizerSerializer, ImageNSFWRecognizerURLSerializer
from .tf_model import OpenNSFWModel

logger = logging.getLogger(__name__)


class NSFWClassifierView(generics.CreateAPIView):
    # TODO: change permissions after testing
    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = ImageNSFWRecognizerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data, request.FILES)
        serializer.is_valid(raise_exception=True)
        image_inmemory_file = serializer.validated_data['image']
        logger.info('Processing image name="%s"', image_inmemory_file.name)
        classifier = NSFWImageClassifier(settings.NSFW_MODEL_WEIGHTS_FILE,
                                         OpenNSFWModel())
        # TODO: Add error processing (what errors may be handled?)
        nsfw_rate = classifier.predict(image_inmemory_file)
        return response.Response({'nsfw_rate': nsfw_rate})


class NSFWClassifierURLView(generics.CreateAPIView):
    # TODO: change permissions after testing
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = ImageNSFWRecognizerURLSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']

        req = requests.get(url)
        file = ContentFile(req.content)

        # image.write(str(req.content))
        name = os.path.basename(url)
        im = InMemoryUploadedFile(file=file, field_name=None, name=name, content_type=req.headers['Content-Type'], size=req.headers['Content-Length'], charset=None)

        # r = requests.get(url, stream=True)
        # r.raw.decode_content = True # Content-Encoding
        # im = Image.open(r.raw) # NOTE: it requires pillow 2.8+

        image_inmemory_file = im
        logger.info('Processing image name="%s"', image_inmemory_file.name)
        classifier = NSFWImageClassifier(settings.NSFW_MODEL_WEIGHTS_FILE,
                                         OpenNSFWModel())
        # TODO: Add error processing (what errors may be handled?)
        nsfw_rate = classifier.predict(image_inmemory_file)
        return response.Response({'nsfw_rate': nsfw_rate})
