import tensorflow as tf
from lib.nn_model_base import NN
from tf_models.lstm import LSTM
from tf_metrics.multi_label_classification import tf_accuracy, tf_precision, tf_recall, tf_f1, tf_hamming_loss


keras = tf.keras
layers = keras.layers


class Model(NN):
    params = {
        **NN.default_params,
        'learning_rate': 1e-3,
        'emb_dim': 128,
        'hidden_units': 128,
        # 'lr_decay_rate': 0.01,
        # 'lr_staircase': False,
        # 'lr_factor': 0.6,
        # 'lr_patience': 10,
        'batch_size': 64,
        'epoch': 3000,
        'early_stop': 100,
        'monitor': 'val_tf_f1',
        'monitor_mode': 'max',
        'monitor_start_train': 'tf_accuracy',
        'monitor_start_train_val': 0.70,
        'dropout': 0.0,
        # 'kernel_initializer': 'glorot_uniform',
        'loss': 'categorical_crossentropy',
        # 'loss': 'mean_squared_error',
        # 'loss': 'mean_squared_error + categorical_crossentropy',
    }

    def __init__(self, input_dim, model_dir, model_name=None, num_classes=None):
        self.__input_dim = input_dim
        self.__num_classes = num_classes
        super(Model, self).__init__(model_dir, model_name, num_classes)

    # @staticmethod
    def self_defined_loss(self, y_true, y_pred, from_logits=False, label_smoothing=0):
        return keras.losses.categorical_crossentropy(y_true, y_pred, True, 0.1)
        # return keras.losses.categorical_crossentropy(y_true, y_pred, from_logits, label_smoothing) / float(self.num_classes)

        # return keras.losses.mean_squared_error(y_true, y_true * y_pred + (1 - y_true) * y_pred) + \
        #        keras.losses.categorical_crossentropy(y_true, y_pred, from_logits, label_smoothing) * 0.002
        # return keras.losses.mean_squared_error(y_true, (1 - y_true) * y_pred)

    @property
    def config_for_keras(self):
        return {
            'optimizer': tf.train.AdamOptimizer,
            # 'loss': keras.losses.binary_crossentropy,
            # 'loss': keras.losses.categorical_crossentropy,
            'loss': keras.losses.mean_squared_error,
            # 'loss': self.self_defined_loss,
            'metrics': [
                tf_accuracy,
                tf_hamming_loss,
                tf_f1,
                tf_precision,
                tf_recall,
            ],
            'callbacks': [
                self.callback_tf_board,
                self.callback_saver,
                # self.callback_reduce_lr,
            ],
        }

    def build(self):
        """ Build neural network architecture """
        self.model = LSTM(
            input_dim=self.__input_dim,
            emb_dim=self.params['emb_dim'],
            num_class=self.__num_classes,
            hidden_units=self.params['hidden_units'],
            dropout_rate=self.params['dropout'],
            activation='tanh',
        )
