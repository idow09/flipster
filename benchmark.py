import numpy as np
# noinspection PyPackageRequirements,PyUnresolvedReferences
from functional import seq

from utils import *


def parse_labels(labels_path):
    return {path: label.strip().lower() == 'true' for path, label in seq.csv(labels_path).list()}


class Benchmark(object):
    def __init__(self, images_root, labels_path, preds_path) -> None:
        self.image_paths = seq(load_image_paths(images_root))
        self.labels = parse_labels(labels_path)
        self.preds = parse_labels(preds_path)
        pos = self.image_paths.filter(self._positive)
        noisy = self.image_paths.filter(self._noisy)
        true_pos = pos.filter(self._true)
        self.precision = true_pos.len() / pos.len() if pos.len() > 0 else 1.0
        self.recall = true_pos.len() / noisy.len() if noisy.len() > 0 else 1.0
        print('precision: {}'.format(self.precision))
        print('recall: {}'.format(self.recall))

    def _true(self, p):
        return self.labels[p] == self.preds[p]

    def _positive(self, p):
        return self.preds[p]

    def _noisy(self, p):
        return self.labels[p]

    def path2sample(self, p):
        return {'path': p, 'label': self.labels[p], 'pred': self.preds[p]}

    @staticmethod
    def positive(sample):
        return sample['pred']

    @staticmethod
    def negative(sample):
        return not Benchmark.positive(sample)

    @staticmethod
    def true(sample):
        return sample['label'] == sample['pred']

    @staticmethod
    def false(sample):
        return not Benchmark.true(sample)

    @staticmethod
    def noise(sample):
        return sample['label']

    @staticmethod
    def not_noise(sample):
        return not Benchmark.noise(sample)

    @staticmethod
    def true_positive(sample):
        return Benchmark.true(sample) and Benchmark.positive(sample)

    @staticmethod
    def true_negative(sample):
        return Benchmark.true(sample) and Benchmark.negative(sample)

    @staticmethod
    def false_positive(sample):
        return Benchmark.false(sample) and Benchmark.positive(sample)

    @staticmethod
    def false_negative(sample):
        return Benchmark.false(sample) and Benchmark.negative(sample)

    def choose_samples(self, cond=lambda s: True, num_samples=9):
        candidates = self.image_paths.map(self.path2sample).filter(cond).list()
        return candidates if len(candidates) < num_samples \
            else list(np.random.choice(candidates, num_samples, replace=False))

    def count_samples(self, cond=lambda s: True):
        return self.image_paths.map(self.path2sample).filter(cond).len()
