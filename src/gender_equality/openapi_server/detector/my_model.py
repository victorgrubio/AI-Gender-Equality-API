import tensorflow as tf
from keras.models import load_model, model_from_json

class MyModel:
    @staticmethod
    def load_model(path_weights=None, path_arch=None, model=None):
        if model is not None:
            model = model
            if path_weights is not None:
                model.load_weights(path_weights)
                return model
        else:
            if path_arch is None:
                return load_model(path_weights)
            else:
                model = None
                with open(path_arch, 'r') as f:
                    model = model_from_json(f.read())
                model.load_weights(path_weights)
                return model

    def __init__(self, path_weights, path_arch=None, model=None):
        self.model = self.load_model(path_weights, path_arch, model)
        self.graph = tf.get_default_graph()

    def predict(self, x):
        with self.graph.as_default():
            return self.model.predict(x)
