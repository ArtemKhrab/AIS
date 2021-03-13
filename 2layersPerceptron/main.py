import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
import pickle
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
(train_x, train_y), (test_x, test_y) = keras.datasets.fashion_mnist.load_data()
models_folder = os.curdir + "/models/"

labelNames = ["top", "trouser", "pullover", "dress", "coat",
              "sandal", "shirt", "sneaker", "bag", "ankle boot"]

INPUT_SHAPE = 784
NUM_CATEGORIES = 10


def fit_model(train_x_, train_y_, test_x_, test_y_, model_):
    model_.fit(train_x_,
               train_y_,
               epochs=8,
               batch_size=32,
               validation_data=(test_x_, test_y_))
    pickle.dump(model_, open(f'{models_folder}model.sav', 'wb'))


if __name__ == '__main__':

    train_x = train_x.reshape(60000, 28 * 28)
    test_x_normalized = test_x.reshape(10000, 28 * 28)
    train_x = train_x.astype('float32') / 255
    test_x_normalized = test_x_normalized.astype('float32') / 255

    train_y = keras.utils.to_categorical(train_y)
    test_y_normalized = keras.utils.to_categorical(test_y)

    # model = Sequential()
    #
    # model.add(Dense(512, input_dim=INPUT_SHAPE))
    # model.add(Activation('relu'))
    #
    # model.add(Dense(NUM_CATEGORIES))
    # model.add(Activation('softmax'))
    #
    # model.compile(optimizer='rmsprop',
    #               loss='categorical_crossentropy',
    #               metrics=['accuracy'])
    #
    # fit_model(train_x, train_y, test_x_normalized, test_y_normalized, model)

    model = pickle.load(open(f'{models_folder}model.sav', 'rb'))

    prediction = model.predict(test_x_normalized)

    labels = np.argmax(prediction, 1)
    for x, y, z in list(zip(test_x, test_y, labels)):
        plt.title(f"Predicted: {labelNames[z]}; From table: {labelNames[y]}")
        plt.imshow(x)
        plt.show()
        cmd = str(input()).lower()
        if cmd == "q":
            break
