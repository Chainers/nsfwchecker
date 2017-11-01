from django.conf.urls import url

from .views import NSFWClassifierView, NSFWClassifierURLView


urlpatterns = [
    url(r'^nsfw_recognizer',
        NSFWClassifierView.as_view(),
        name='nsfw-recognizer'),
    url(r'^nsfw_url_recognizer',
        NSFWClassifierURLView.as_view(),
        name='nsfw-recognizer-url'),
]
