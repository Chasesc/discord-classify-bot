import argparse
import config

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from fastai import metrics

from fastai.train import ClassificationInterpretation

from fastai.vision import learner
from fastai.vision import models
from fastai.vision import transform

from fastai.vision.image import open_image
from fastai.vision.data import ImageDataBunch, verify_images, imagenet_stats

PATH = Path(config.get('save_path'))
TRAIN_PATH = PATH / 'train'
MODEL_NAME = 'current_model'

def load_model(inference=False):
    if inference:
        data = ImageDataBunch.load_empty(TRAIN_PATH)
    else:
        np.random.seed(1337) # give consistency to the validation set
        data = ImageDataBunch.from_folder(TRAIN_PATH, train=".", valid_pct=0.1,
            ds_tfms=transform.get_transforms(), size=224, num_workers=4, bs=32).normalize(imagenet_stats)

        data.export() # Save the classes used in training for inference
        
    learn = learner.cnn_learner(data, models.resnet34, metrics=metrics.error_rate)
    
    if inference:
        learn.load(MODEL_NAME)

    return learn, data

def verify():
    for c in TRAIN_PATH.iterdir():
        num_items = len(list(c.glob('*')))
        if c.is_dir() and c.parts[-1] != 'models' and num_items >= 1:
            verify_images(c, delete=True, max_size=500)

def train(num_epochs, interp):
    verify()

    learn, data = load_model()

    print('classes:', data.classes)

    learn.fit_one_cycle(num_epochs)
    learn.save(MODEL_NAME)

    if interp:
        interpret(learn)

def predict(img_path):
    learn, data = load_model(inference=True)

    img = open_image(img_path)
    pred_class, pred_idx, outputs = learn.predict(img)

    zipped = zip((round(n, 3) for n in map(float, outputs)), data.classes)
    zipped = sorted(zipped, key=lambda tup:tup[0], reverse=True)
    
    print(f'Predicted Class: {pred_class}')
    print(f'Probs: {zipped}')

def interpret(learn):
    interp = ClassificationInterpretation.from_learner(learn)
    
    interp.plot_confusion_matrix()
    plt.savefig(PATH / 'confusion_matrix.jpg')

    interp.plot_top_losses(8)
    plt.savefig(PATH / 'top_losses.jpg')


parser = argparse.ArgumentParser()
parser.add_argument('--train', action='store_true', default=False, help='should we train?')
parser.add_argument('--interp', action='store_true', default=False, help='should we interpret the results of our model?')
parser.add_argument('--num_epochs', default=5, help='how many epochs to train on')
parser.add_argument('--img_path', default='', help='path of the image to predict')
args = parser.parse_args()

if args.train:
    train(args.num_epochs, args.interp)
else:
    predict(args.img_path)