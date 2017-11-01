import os

from django.urls import reverse
from rest_framework.test import APITestCase


FIXTURE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'test_fixtures')
NSFW_IMAGE = os.path.join(FIXTURE_DIR, 'nsfw.jpg')
NON_NSFW_IMAGE = os.path.join(FIXTURE_DIR, 'non_nsfw.jpg')


class NSFWRecognitionAPITestCase(APITestCase):

    NSFW_ENDPOINT = reverse('nsfw_recognizer:nsfw-recognizer')

    def _upload_image_for_recognition(self, filepath, image_field='image'):
        """
        :param filepath: absolute path to the file to be uploaded
        :param image_field: name of the field used in the request
        """
        with open(filepath, 'rb') as fp:
            return self.client.post(self.NSFW_ENDPOINT, {image_field: fp})

    def test_uploading_nude_picture_returns_high_nsfw_rate(self):
        resp = self._upload_image_for_recognition(NSFW_IMAGE)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['nsfw_rate'] > 0.9)

    def test_uploading_neutral_picture_returns_low_nsfw_rate(self):
        resp = self._upload_image_for_recognition(NON_NSFW_IMAGE)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['nsfw_rate'] < 0.9)

    def test_uploading_body_with_no_image_raises_validation_error(self):
        resp = self._upload_image_for_recognition(NON_NSFW_IMAGE,
                                                  image_field='sdad')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'image': ['No file was submitted.']})
