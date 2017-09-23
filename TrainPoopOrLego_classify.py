#to manage and convert the images
from scipy.misc import imsave, imread, imresize
#for matrixes etc
import numpy as np
#to hold our model
import keras.models
#for reg exprs
import re
#for file operations
import sys
import os
from keras import backend as K

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

# dimensions of our images.
img_width, img_height = 150, 150


#defines where the model directory is and loads the files in there
sys.path.append(os.path.abspath('./model'))
from load import *

#create and load the model and graph
global model, graph
model, graph = init('./model/poop_model')


if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


#test_model = load_model('./model/poop_model.h5')
img = load_img('./test.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
#print(x)
x = np.expand_dims(x, axis=0)
#print(x)
preds = model.predict_classes(x)
print('preds')
print(preds)
prob = model.predict_proba(x)
print('probs')
print(prob)
print(preds, prob)


