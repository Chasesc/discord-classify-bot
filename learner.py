import argparse

from pathlib import Path

from fastai import metrics

from fastai.vision import learner
from fastai.vision import models
from fastai.vision import transform

from fastai.vision.image import open_image
from fastai.vision.data import ImageDataBunch, verify_images, imagenet_stats

TRAIN_PATH = Path('/media/chases/6CACED15ACECDA9A/discord_bot_files/whois/train')

def verify():
    for c in TRAIN_PATH.iterdir():
        num_items = len(list(c.glob('*')))
        if c.is_dir() and c.parts[-1] != 'models' and num_items >= 1:
            verify_images(c, delete=True, max_size=500)

def train(num_epochs):
    verify()

    data = ImageDataBunch.from_folder(TRAIN_PATH, train=".", valid_pct=0.1,
        ds_tfms=transform.get_transforms(), size=224, num_workers=4, bs=32).normalize(imagenet_stats)

    data.export()

    print('classes:', data.classes)
    learn = learner.cnn_learner(data, models.resnet34, metrics=metrics.error_rate)

    learn.fit_one_cycle(num_epochs)
    learn.save('current_model')

    #with open(TRAIN_PATH / 'models/classes', 'w') as f:
    #    f.write(data.classes)

def predict(img_path):
    data = ImageDataBunch.load_empty(TRAIN_PATH)
    learn = learner.cnn_learner(data, models.resnet34, metrics=metrics.error_rate)
    learn.load('current_model')

    img = open_image(img_path)
    pred_class,pred_idx,outputs = learn.predict(img)
    print(f'Predicted Class: {pred_class}')
    zipped = zip((round(n, 3) for n in map(float, outputs)), data.classes)
    zipped = sorted(zipped, key=lambda tup:tup[0], reverse=True)
    print(f'Probs: {zipped}')



parser = argparse.ArgumentParser()
parser.add_argument('--train', action='store_true', default=False, help='should we train?')
parser.add_argument('--num_epochs', default=5, help='how many epochs to train on')
parser.add_argument('--img_path', default='', help='path of the image to predict')
args = parser.parse_args()

if args.train:
    train(args.num_epochs)
else:
    predict(args.img_path)