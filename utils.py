import glob
import os

# noinspection PyPackageRequirements
from functional import seq


def load_image_paths(path_or_txt):
    """
    Loads a list of image paths from a given resource
    :param path_or_txt: A path to an image, a directory containing images, or to a txt file containing image paths.
    :return: A list of image paths.
    """
    img_formats = ['.jpg', '.jpeg', '.png', '.tif']

    if os.path.isdir(path_or_txt):
        files = (seq(path_or_txt)
                 .map(lambda d: '%s/*.*' % d)
                 .flat_map(glob.glob))
    elif os.path.isfile(path_or_txt):
        if path_or_txt.endswith('.txt'):
            with open(path_or_txt, 'r') as file:
                files = (seq(file.readlines())
                         .map(str.strip))
        else:
            files = seq(path_or_txt)
    else:
        files = seq([])

    return (files
            .filter(lambda f: os.path.splitext(f)[-1].lower() in img_formats)
            .sorted()
            .list())


def auto_str(cls):
    """
    Annotate a class @auto_str to have it pretty-printed whenever you str() it
    """

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls
