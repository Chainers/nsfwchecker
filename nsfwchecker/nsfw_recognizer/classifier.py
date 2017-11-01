# Code here is an apapted version of the code
# in this repo: https://github.com/mdietrichstein/tensorflow-open_nsfw
# TF model is taken AS-IS
import io
import logging
import time

import skimage
import skimage.io
import numpy as np
import tensorflow as tf

from PIL import Image


class NSFWImageClassifier(object):

    VGG_MEAN = [104, 117, 123]

    def __init__(self,
                 model_weights_file: str,
                 model):
        """
        :param model_weights_file: absolute path to
        neural network weights file
        """
        self.log = logging.getLogger(__name__)
        self._model = model
        self._weights_file = model_weights_file

    def _prepare_image(self, data, size=(256, 256)):
        """
        Resize image. Please use this resize logic for
        best results instead of the caffe,
        since it was used to generate training dataset
        """
        im = Image.open(data)
        if im.mode != "RGB":
            im = im.convert('RGB')
        imr = im.resize(size, resample=Image.BILINEAR)
        fh_im = io.BytesIO()
        # Only JPEG images are supported
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)

        image = (skimage
                 .img_as_float(skimage.io.imread(fh_im, as_grey=False))
                 .astype(np.float32))

        H, W, _ = image.shape
        h, w = (224, 224)

        h_off = max((H - h) // 2, 0)
        w_off = max((W - w) // 2, 0)
        image = image[h_off:h_off + h, w_off:w_off + w, :]

        # RGB to BGR
        image = image[:, :, :: -1]

        image = image * 255

        image -= self.VGG_MEAN

        image = np.expand_dims(image, axis=0)
        return image

    def predict(self, img: Image):
        """
        Run a Tensorflow network on an input image after preprocessing.
        :param PIL.Image img:
            PIL image to be input into TF.
        """
        __time_started = time.monotonic()
        prepared_img = self._prepare_image(img)
        self.log.info('Image preprocessed for %s seconds.',
                      time.monotonic() - __time_started)

        computation_graph = tf.Graph()
        with tf.Session(graph=computation_graph) as session:
            self.log.debug('Building model with weights file "%s"',
                           self._weights_file)
            self._model.build(weights_path=self._weights_file)
            session.run(tf.global_variables_initializer())
            predictions = \
                session.run(self._model.predictions,
                            feed_dict={self._model.input: prepared_img})
            __time_finished = time.monotonic()
            self.log.info('Image processing took %s seconds',
                          __time_finished - __time_started)
            self.log.info('Prediction result: %s', predictions[0][1])
            return predictions[0][1]
