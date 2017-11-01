from django.conf.urls import url

from .views import NSFWClassifierView


urlpatterns = [
    url(r'^nsfw_recognizer',
        NSFWClassifierView.as_view(),
        name='nsfw-recognizer'),
]
