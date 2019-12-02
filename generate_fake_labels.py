import random
from utils import load_image_paths

image_paths = load_image_paths('/home/idow09/DEV/Flipster/DemoDataset/images')
with open('/home/idow09/DEV/Flipster/DemoDataset/labels.txt', 'w') as labels:
    for path in image_paths:
        labels.write('{},{}\n'.format(path, random.random() < 0.13))
