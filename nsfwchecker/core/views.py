from django.conf import settings
from django.views.generic import TemplateView

from rest_framework import generics, permissions, response, parsers
from rest_framework.authentication import SessionAuthentication

from nsfwchecker.nsfw_recognizer.serializers import ImageNSFWRecognizerSerializer, ImageNSFWRecognizerURLSerializer
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

