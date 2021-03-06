import tensorflow as tf

# tf.enable_eager_execution()
import numpy as np

keras = tf.keras
layers = keras.layers


class LSTM(keras.Model):

    def __init__(self, input_dim, emb_dim, num_class, hidden_units=500, dropout_rate=0.0, activation='tanh',
                 name='lstm'):
        super(LSTM, self).__init__(name=name)
        self.__ranges = np.expand_dims(np.arange(input_dim), axis=0)
        self.__emb = layers.Embedding(input_dim, emb_dim)

        self.__lstm_1 = layers.LSTM(hidden_units, return_sequences=True, return_state=True, dropout=dropout_rate)
        self.__lstm_2 = layers.LSTM(hidden_units, dropout=dropout_rate)
        self.__fc_3 = layers.Dense(hidden_units, activation=activation)
        self.__dropout = layers.Dropout(dropout_rate)
        self.__fc_4 = layers.Dense(num_class, activation=activation)

    def __get_emb(self, x_mask):
        x_mask = tf.expand_dims(tf.cast(x_mask, tf.float32), axis=-1)
        embeddings = self.__emb(self.__ranges) * x_mask
        embeddings = tf.reduce_sum(embeddings, axis=-2)
        return embeddings

    def call(self, inputs, training=None, mask=None):
        embeddings = self.__get_emb(inputs)

        x, final_memory_state, final_carry_state = self.__lstm_1(embeddings, training=training)
        x = self.__lstm_2(x, training=training)
        x = self.__fc_3(x)
        x = self.__dropout(x, training=training)
        x = self.__fc_4(x)

        return x


# a = np.array([[3, 2, 2, 0, 1], [0, 0, 1, 3, 0]])
# b = np.array([[0, 0, 0, 1, 1], [0, 1, 1, 0, 0]])
# aa = np.array([a, a, a, b, b, a])
# # c = [a, b]
#
# lstm_layer = LSTM(5, 3, 5, 10, 0.2)
# _input = lstm_layer(aa)
#
# print('!!!!!!!!!!!!!!!!!!!!!')
# print(_input)
