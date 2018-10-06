# -*- coding: utf-8 -*-
"""
Project: Automatic Collage Maker using FLASK API and PIL
Program by :
@author    : Pranav Gundewar
"""
# Importing Libraries
from argparse import ArgumentParser
import os
import random
from PIL import Image
from os.path import isfile, isdir
from sys import exit
from PIL.ExifTags import TAGS
import time


class ImageProcess:
    """
    Abstract base class for image file processors and collage creation.
    """

    def __init__(self):
        self.extensions = ['.jpg', '.jpeg', '.png']

    def processdir(self, filename):
        """
                Creates the list of all the files with given extensions
                and returns list and filecount
        """
        filecount = 0  # Number of files successfully updated
        count = 0   # Number of images successfully updated
        files = []
        images = []
        for fn in os.listdir(filename):
            print("Processing %s" % fn)
            files.append(os.path.join(filename, fn))
            filecount += 1

        for fn in files:
            for ext in self.extensions:
                if os.path.splitext(fn)[1].lower() == ext:
                    images.append(fn)
                    count += 1

        image_list = []
        for img_path in images:
            img = Image.open(img_path)
            img = self.reorient_image(img)
            image_list.append(img)
        return count, image_list

    def reorient_image(self, image):
        """
        Re-orient image to required orientation to create collages
        """
        try:
            if hasattr(image, '_getexif'):  # only present in JPEGs
                for orientation in TAGS.keys():
                    if TAGS[orientation] == 'Orientation':
                        break
                e = image._getexif()       # returns None if no EXIF data
                if e is not None:
                    exif = dict(e.items())
                    orientation = exif[orientation]
                    # Make changes in the image according to the orientation
                    if orientation == 2:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3:
                        image = image.transpose(Image.ROTATE_180)
                    elif orientation == 4:
                        image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    elif orientation == 5:
                        image = image.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
                    elif orientation == 6:
                        image = image.transpose(Image.ROTATE_270)
                    elif orientation == 7:
                        image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
                    elif orientation == 8:
                        image = image.transpose(Image.ROTATE_90)
        except Exception:
            print('Input image does not have metadata. Moving on..')
            pass
        return image

    def collage_creation(self, coefs_lines, collage_image, width, init_height):
        margin_size = 2
        y = 0
        for coef, images in coefs_lines:
            if images:
                x = 0
                for img in images:
                        # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                    k = (init_height / coef) / img.size[1]
                    if k > 1:
                        img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                    else:
                        img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                    w, h = img.size
                    if(w + x > width):
                        if (int(width - x) > 0):
                            img = img.resize((int(width - x), h), Image.ANTIALIAS)
                    collage_image.paste(img, (int(x), int(y)))
                    x += img.size[0] + margin_size
                y += int(init_height / coef) + margin_size
        w, h = collage_image.size
        collage = Image.new('RGB', (w + margin_size, h + margin_size), (35, 35, 35))
        collage.paste(collage_image, (margin_size, margin_size))
        return collage

    def make_collage(self, images, width, init_height):
        """
        Make a collage image with a width equal to `width` from `images` and save to `filename`.
        """
        margin_size = 2
        # run until a suitable arrangement of images is found
        while True:
            # copy images to images_list
            images_list = images[:]
            coefs_lines = []
            images_line = []
            x = 0
            while images_list:
                # get first image and resize to `init_height`
                img = images_list.pop(0)
                img.thumbnail((width, init_height), Image.ANTIALIAS)
                # when `x` will go beyond the `width`, start the next line
                if x > width:
                    coefs_lines.append((float(x) / width, images_line))
                    images_line = []
                    x = 0
                x += img.size[0] + margin_size
                images_line.append(img)
            # finally add the last line with images
            coefs_lines.append((float(x) / width, images_line))

            # compact the lines, by reducing the `init_height`, if any with one or less images
            if len(coefs_lines) <= 1:
                break
            if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
                # reduce `init_height`
                init_height -= 10
            else:
                break
        print('Suitable arrangement of images has been found out..')

        # get output height
        out_height = 0
        for coef, imgs_line in coefs_lines:
            if imgs_line:
                out_height += int(init_height / coef) + margin_size
        if not out_height:
            print('Height of collage could not be 0!')
            return False

        collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
        print('Dimension of background canvas has been obtained..')
        # put images to the collage
        # Call self function to access functions in the same class
        collage_image = self.collage_creation(coefs_lines, collage_image, width, init_height)
        # Putting timestamp to the image output filename
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = 'collage' + timestr + '.jpg'
        collage_image.save(filename, quality=95)
        return True


if __name__ == "__main__":
    # Argument parsing
    parser = ArgumentParser(description='Automatic Photo Collage Maker.')
    parser.add_argument('-f', '--folder', dest='folder',
                        help='folder with images (*.jpg, *.jpeg, *.png)', default='.')

    args = parser.parse_args()
    # create an instance of defined class
    process = ImageProcess()
    # Run according to whether path is a file or a directory
    if isfile(args.folder):
        print('Please provide different directory containing at-least 2 images.. ')
        exit(1)
    elif isdir(args.folder):
        count, images = process.processdir(args.folder)
        print('\nNumber of Input Images: ' + str(count) + '\n')

    # shuffle images if needed
    random.shuffle(images)

    if(count < 6):
        res = process.make_collage(images, 1200, 450)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 1 has been created.')
        time.sleep(1)   # delays for 1 second
        random.shuffle(images)
        res = process.make_collage(images, 1150, 375)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 2 has been created.')
        time.sleep(1)   # delays for 1 second
        random.shuffle(images)
        res = process.make_collage(images, 1200, 425)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 3 has been created.')

    if (count > 6):
        res = process.make_collage(images, 800, 300)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 1 has been created.')
        time.sleep(1)   # delays for 1 second
        random.shuffle(images)
        res = process.make_collage(images, 1000, 250)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 2 has been created.')
        time.sleep(1)   # delays for 1 second
        random.shuffle(images)
        res = process.make_collage(images, 800, 350)
        if not res:
            print('Failed to create collage!')
            exit(1)
        print('Collage 3 has been created.')
    print('Your collages are ready. Head over to the Gallery.. ')
