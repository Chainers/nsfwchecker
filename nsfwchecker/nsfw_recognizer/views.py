import logging
import os

from django.conf import settings
from rest_framework import (
    generics,
    parsers,
    permissions,
    response,
)

from .classifier import NSFWImageClassifier
from .serializers import ImageNSFWRecognizerSerializer
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
