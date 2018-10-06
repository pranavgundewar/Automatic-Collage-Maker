# -*- coding: utf-8 -*-
"""
Project:    Automatic Collage Maker
Script:     Abstract base class for image processing
@author:    Pranav Gundewar
"""
# Importing Libraries
import os
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import time
import numpy as np
import cv2


class ImageProcess():
    """
    Abstract base class for image file processors and collage creation.
    """

    def __init__(self):
        self.extensions = ['.jpg', '.jpeg', '.png']
        # self.output_width = 1200
        # self.output_height = 800

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
            # print("Processing %s" % fn)
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
            # img.thumbnail([2400, 2400], Image.ANTIALIAS)
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

    def timestamp(self):
        """
        This creates timestamp string which can be used for naming purposes
        """
        now = time.time()
        localtime = time.localtime(now)
        milliseconds = '%02d' % int((now - int(now)) * 1000)
        return time.strftime('%Y%m%d-%H%M%S', localtime) + milliseconds

    def draw_text(self, img, text, font_size, location):
        """
        Draw lines, points, ellipses, rectangles, shapes and text.
        Parameters: text - The text that you would like to print on an image
                    color - color of text
                    font_size - size of the text
                    location - tuple(width, height) where you would like to print on the image
        """

        font = ImageFont.truetype("Fonts/arial.ttf", font_size)
        width, height = img.size
        img_draw = ImageDraw.Draw(img)
        line_height = font.getsize(text)[1]
        line_width = font.getsize(text)[0]
        margin = 20
        color = self.color_chooser(img, line_height, line_width, location)
        if location == 'bottom left':
            coord = (margin, height - line_height - margin)
        elif location == 'top right':
            coord = (width - line_width - margin, margin)
        else:
            coord = (width - line_width - margin, height - line_height - margin)
        img_draw.text(coord, text, fill=color, font=font)
        return img

    def put_logo(self, img, text, font_size, location):
        """
        This function allows to put transparent logo on the image
        """
        font = ImageFont.truetype("Fonts/Verdana.ttf", font_size)
        width, height = img.size
        img_draw = ImageDraw.Draw(img)
        line_height = font.getsize(text)[1]
        line_width = font.getsize(text)[0]
        margin = 20
        color = self.color_chooser(img, line_height, line_width, location)
        coord = (width - line_width - margin, height - line_height - margin)
        if color == 'black':
            img_draw.text(coord, text, fill=color, font=font)
        else:
            img_draw.text(coord, text, fill=color, font=font)

        return img

    def brightness(self, pixel):
        """
        This function calculates the brightness intensity perceived for the human vision
        """
        return (pixel[0] * 299 + pixel[1] * 587 + pixel[2] * 114) / 1000

    def contrast(self, pixel):
        """
        This function determines whether background is dark or white
        """
        return (self.brightness(pixel) > 123)

    def color_chooser(self, image, line_height, line_width, location):
        """
        This function determines the contrast color for the text according to background
        Returns the color of contrast text
        """
        width, height = image.size
        f = 0
        t = 0
        if location == 'bottom left':
            for i in range(line_width):
                for j in range(height - line_height, height):
                    pixel = image.getpixel((i, j))
                    b = self.contrast(pixel)
                    if b is False:
                        f += 1
                    else:
                        t += 1
        elif location == 'top right':
            for i in range(width - line_width, width):
                for j in range(line_height):
                    pixel = image.getpixel((i, j))
                    b = self.contrast(pixel)
                    if b is False:
                        f += 1
                    else:
                        t += 1
        else:
            for i in range(width - line_width, width):
                for j in range(height - line_height, height):
                    pixel = image.getpixel((i, j))
                    b = self.contrast(pixel)
                    if b is False:
                        f += 1
                    else:
                        t += 1
        if f > t:
            return 'white'
        else:
            return 'black'

    def image_location(self, image, place, x):
        if place == 'left':
            image = image.crop((x - 200, 0, image.size[0], image.size[1]))
            bg = Image.new('RGB', (1200, 800), (255, 255, 255))
            bg.paste(image, (0, 0))
            # bg.show()
        else:
            image = image.crop((x - 300, 0, x + 400, image.size[1]))
            bg = Image.new('RGB', (1200, 800), (255, 255, 255))
            bg.paste(image, (500, 0))
            # bg.show()
        return bg

    def face_location(self, image, position):
        """
        This function finds the location of face in an image which will help
        us determine cropping conditoin
        """
        point1 = (500, 600)
        point2 = (500, 200)
        point3 = (700, 600)
        point4 = (700, 200)
        p = (0, 0)
        face_cascade = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
        image = np.array(image)
        # Convert RGB to BGR
        image = image[:, :, ::-1].copy()
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(grayImage,
                                              scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(80, 80),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) == 0:
            print("No faces found")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            return image
        else:
            # print("Number of faces detected: " + str(faces.shape[0]))
            m = []
            for i in range(len(faces)):
                m.append(faces[i][2])
            n = np.argmax(m)
            array = faces[n]
            # print(array)
            box = [array]
            for (x, y, w, h) in box:
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                newpoint1 = (x + w, y)
                newpoint2 = (x + w, y + h)
                newpoint3 = (x, y + h)
                newpoint4 = (x, y)
                op1 = tuple(x - y for x, y in zip(point1, newpoint1))
                op2 = tuple(x - y for x, y in zip(point2, newpoint2))
                op3 = tuple(x - y for x, y in zip(newpoint3, point3))
                op4 = tuple(x - y for x, y in zip(newpoint4, point4))
                if op1 > p and op2 > p:
                    # print('Face Lies in left zone')
                    location = 'left'
                elif op3 > p and op4 > p:
                    # print('Face lies in the right zone')
                    location = 'right'
                else:
                    location = 'middle'
                    # print('Face lies in middle')
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                if location != 'right' and position == 'right':
                    image = self.image_location(image, 'right', x)
                elif location != 'left' and position == 'left':
                    image = self.image_location(image, 'left', x)

                return image

    def face_detection(self, image, output_width, output_height):
        """
        This function finds the location of face in an image which will help
        us determine cropping conditoin
        """
        face_cascade = cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
        image = np.array(image)
        # Convert RGB to BGR
        image = image[:, :, ::-1]
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(grayImage,
                                              scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(90, 90),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) == 0:
            image = self.image_crop(image, 200, 0, 150, 150, output_width, output_height)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
        else:
            m = []
            for i in range(len(faces)):
                m.append(faces[i][2])
            n = np.argmax(m)
            array = faces[n]
            box = [array]
            for (x, y, w, h) in box:
                image = self.image_crop(image, x, y, w, h, output_width, output_height)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)

        return image

    def image_crop(self, image, x, y, w, h, output_width, output_height):
        height, width = image.shape[:2]
        newWidth = int((output_width - w) / 2)
        newHeight = int((output_height - h) / 2)
        if x - newWidth > 0:
            if x - newWidth + output_width < width:
                x1 = x - newWidth
                if y - newHeight > 0:
                    if y - newHeight + output_height < height:
                        y1 = y - newHeight
                    else:
                        y1 = height - output_height
                else:
                    y1 = 0
            else:
                x1 = width - output_width
                if y - newHeight > 0:
                    if y - newHeight + output_height < height:
                        y1 = y - newHeight
                    else:
                        y1 = height - output_height
                else:
                    y1 = 0
        else:
            x1 = 0
            if y - newHeight > 0:
                if y - newHeight + output_height < height:
                    y1 = y - newHeight
                else:
                    y1 = height - output_height
            else:
                y1 = 0

        image = image[y1:y1 + output_height, x1:x1 + output_width]
        # image = image.crop((x1, y1, x1 + output_width, y1 + output_height))
        return image

    def collage_creation(self, coefs_lines, collage_image, width, init_height):
        margin_size = 0
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
        collage = Image.new('RGB', (w + margin_size, h + margin_size), (0, 0, 0))
        collage.paste(collage_image, (margin_size, margin_size))

        return collage

    def make_collage(self, images, width, init_height):
        """
        Make a collage image with a width equal to `width` from `images` and save to `filename`.
        """
        margin_size = 0
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

        collage_image = Image.new('RGB', (width, int(out_height)), (0, 0, 0))
        print('Dimension of background canvas has been obtained..')
        collage_image = self.collage_creation(coefs_lines, collage_image, width, init_height)
        # Putting timestamp to the image output filename
        timestr = self.timestamp()
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(self.output, filename)
        collage_image = self.put_logo(collage_image, 'HauteBook', 30, 'bottom right')
        collage_image.save(filename, quality=90, optimize=True)
        return True
