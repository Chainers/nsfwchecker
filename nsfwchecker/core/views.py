from django.conf import settings
from django.views.generic import TemplateView

from rest_framework import generics, permissions, response, parsers
from rest_framework.authentication import SessionAuthentication

from nsfwchecker.nsfw_recognizer.serializers import ImageNSFWRecognizerSerializer
from nsfwchecker.nsfw_recognizer.classifier import NSFWImageClassifier
from nsfwchecker.nsfw_recognizer.tf_model import OpenNSFWModel


class ExemptCSRFSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class IndexView(TemplateView):
    template_name = 'index.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        # kwargs['form'] = ImageForm()
        return super(IndexView, self).get_context_data(**kwargs)


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
        classifier = NSFWImageClassifier(settings.NSFW_MODEL_WEIGHTS_FILE,
                                         OpenNSFWModel())
        # TODO: Add error processing (what errors may be handled?)
        nsfw_rate = classifier.predict(image_inmemory_file)
        return response.Response({'nsfw_rate': nsfw_rate})
