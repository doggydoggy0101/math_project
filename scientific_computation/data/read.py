import struct
import numpy as np
from array import array

class MnistDataloader(object):
    ''' Load MNIST dataset '''
    def __init__(self):
        self.training_images_filepath = 'data/MNIST/train-images.idx3-ubyte'
        self.training_labels_filepath = 'data/MNIST/train-labels.idx1-ubyte'
        self.test_images_filepath = 'data/MNIST/t10k-images.idx3-ubyte'
        self.test_labels_filepath = 'data/MNIST/t10k-labels.idx1-ubyte'

    def read_images_labels(self, images_filepath, labels_filepath):        
        labels = []
        with open(labels_filepath, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049, got {}'.format(magic))
            labels = array("B", file.read())        
        
        with open(images_filepath, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051, got {}'.format(magic))
            image_data = array("B", file.read())       

        images = []
        for i in range(size):
            images.append([0] * rows * cols)
        for i in range(size):
            img = np.array(image_data[i * rows * cols:(i + 1) * rows * cols])
            img = img.reshape(28, 28)
            images[i][:] = img            
        
        return images, labels
            
    def load_data(self):
        ''' return x_train, y_train, x_test, y_test'''
        x_train, y_train = self.read_images_labels(self.training_images_filepath, self.training_labels_filepath)
        x_test, y_test = self.read_images_labels(self.test_images_filepath, self.test_labels_filepath)
        
        return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test) 