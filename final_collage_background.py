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
from PIL import Image, ImageDraw, ImageFont
from os.path import isfile, isdir
from sys import exit
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
            # print(faces)
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
                # print(op1, op2)
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
            # print("No faces found")
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


class CollageCreation(ImageProcess):
    """
    Abstract master class for collage creation using diferent layouts.
    """

    def __init__(self):
        # self.extensions = ['.jpg', '.jpeg', '.png']
        ImageProcess.__init__(self)

    def collage_2_hor(self, list_hor):
        bg = Image.new('RGB', (790, 1085), (255, 255, 255))
        random.shuffle(list_hor)
        horizontal = list_hor[:2]
        flag = 0
        for image in horizontal:
            image = image.resize((780, 535), Image.ANTIALIAS)
            if(flag == 0):
                bg.paste(image, (5, 5))
                flag = 1
            else:
                bg.paste(image, (5, 545))
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        bg = Image.new('RGB', (1200, 800), (255, 255, 255))
        random.shuffle(list_hor)
        horizontal = list_hor[:2]
        flag = 0
        for image in horizontal:
            if(flag == 0):
                image1 = image.resize((1200, 800), Image.ANTIALIAS)
                image1 = ImageProcess.face_location(self, image1, 'left')
                flag = 1
            else:
                image2 = image.resize((1200, 800), Image.ANTIALIAS)
                image2 = ImageProcess.face_location(self, image2, 'right')

        for i in range(bg.size[0]):
            for j in range(bg.size[1]):
                if(4 * i + j <= 2800):
                    pixel = image1.getpixel((i, j))
                    bg.putpixel((i, j), pixel)
                else:
                    pixel = image2.getpixel((i, j))
                    bg.putpixel((i, j), pixel)
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        # plt.imshow(bg)
        # plt.show()
        bg.save(filename, quality=90, optimize=True)

        bg = Image.new('RGB', (1200, 800), (255, 255, 255))
        random.shuffle(list_hor)
        horizontal = list_hor[:2]
        flag = 0
        for image in horizontal:
            if(flag == 0):
                image1 = image.resize((1200, 800), Image.ANTIALIAS)
                image1 = ImageProcess.face_location(self, image1, 'left')
                flag = 1
            else:
                image2 = image.resize((1200, 800), Image.ANTIALIAS)
                image2 = ImageProcess.face_location(self, image2, 'right')

        for i in range(bg.size[0]):
            for j in range(bg.size[1]):
                if(4 * i - j <= 2000):
                    pixel = image1.getpixel((i, j))
                    bg.putpixel((i, j), pixel)
                else:
                    pixel = image2.getpixel((i, j))
                    bg.putpixel((i, j), pixel)
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        # plt.imshow(bg)
        # plt.show()
        bg.save(filename, quality=90, optimize=True)

    def collage_3_hor(self, list_hor, list_ver):
        """
        This function takes an input of horizontal as well as vertical oriented images in separate lists.
        """
        if (len(list_hor) == 0):
            print('Plese provide images with width more than height.')
            exit(1)

        random.shuffle(list_ver)
        random.shuffle(list_hor)
        horizontal = list_hor[0]
        vertical = list_ver[:2]

        bg = Image.new('RGB', (815, 1145), (255, 255, 255))
        horizontal = horizontal.resize((805, 530), Image.ANTIALIAS)
        bg.paste(horizontal, (5, 5))
        flag = 0
        for image in vertical:
            image = image.resize((400, 600))
            if(flag == 0):
                bg.paste(image, (5, 540))
                flag = 1
            else:
                bg.paste(image, (410, 540))
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        random.shuffle(list_ver)
        random.shuffle(list_hor)
        horizontal = list_hor[0]
        vertical = list_ver[:2]

        bg = Image.new('RGB', (800, 1130), (255, 255, 255))
        horizontal = horizontal.resize((805, 530), Image.ANTIALIAS)
        bg.paste(horizontal, (0, 0))
        flag = 0
        for image in vertical:
            image = image.resize((400, 600))
            if(flag == 0):
                bg.paste(image, (0, 530))
                flag = 1
            else:
                bg.paste(image, (400, 530))
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        bg = Image.new('RGB', (815, 1145), (255, 255, 255))
        random.shuffle(list_ver)
        random.shuffle(list_hor)
        horizontal = list_hor[0]
        vertical = list_ver[:2]
        horizontal = horizontal.resize((805, 530), Image.ANTIALIAS)
        bg.paste(horizontal, (5, 610))
        flag = 0
        for image in vertical:
            image = image.resize((400, 600))
            if(flag == 0):
                bg.paste(image, (5, 5))
                flag = 1
            else:
                bg.paste(image, (410, 5))
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        bg = Image.new('RGB', (800, 1130), (255, 255, 255))
        random.shuffle(list_ver)
        random.shuffle(list_hor)
        horizontal = list_hor[0]
        vertical = list_ver[:2]
        horizontal = horizontal.resize((800, 530), Image.ANTIALIAS)
        bg.paste(horizontal, (0, 600))
        flag = 0
        for image in vertical:
            image = image.resize((400, 600))
            if(flag == 0):
                bg.paste(image, (0, 0))
                flag = 1
            else:
                bg.paste(image, (400, 0))
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

    def collage_4(self, image_list):
        """
        This function create 2 layouts for vertical images
        [* *    [* _
         * *]   *_]
        """
        random.shuffle(image_list)
        list1 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (750, 1130), (255, 255, 255))
        for image in list1:
            image = image.resize((360, 550), Image.ANTIALIAS)
            if count == 1:
                bg.paste(image, (10, 10))
            elif count == 2:
                bg.paste(image, (380, 10))
            elif count == 3:
                bg.paste(image, (10, 570))
            else:
                bg.paste(image, (380, 570))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        random.shuffle(image_list)
        list2 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (730, 1120), (255, 255, 255))
        for image in list2:
            image = image.resize((350, 500), Image.ANTIALIAS)
            if count == 1:
                bg.paste(image, (10, 10))
            elif count == 2:
                bg.paste(image, (370, 100))
            elif count == 3:
                bg.paste(image, (10, 520))
            else:
                bg.paste(image, (370, 610))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'top right')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        random.shuffle(image_list)
        list3 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (760, 1140), (255, 255, 255))
        for image in list3:
            image = image.resize((400, 600), Image.ANTIALIAS)
            if count == 1:
                bg.paste(image, (0, 0))
            elif count == 2:
                bg.paste(image, (400, 0))
            elif count == 3:
                bg.paste(image, (0, 600))
            else:
                bg.paste(image, (400, 600))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

    def black_magic(self, image_list):
        random.shuffle(image_list)
        list1 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (735, 1055), (255, 255, 255))
        for image in list1:
            if count == 1:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (5, 5))
            if count == 2:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (330, 450))
            if count == 3:
                image = image.resize((300, 440), Image.ANTIALIAS)
                bg.paste(image, (420, 5))
            else:
                image = image.resize((300, 440), Image.ANTIALIAS)
                bg.paste(image, (15, 610))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

        random.shuffle(image_list)
        list1 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (735, 1055), (255, 255, 255))
        for image in list1:
            if count == 1:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (330, 5))
            if count == 2:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (5, 450))
            if count == 3:
                image = image.resize((300, 440), Image.ANTIALIAS)
                bg.paste(image, (420, 610))
            else:
                image = image.resize((300, 440), Image.ANTIALIAS)
                bg.paste(image, (15, 5))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

    def portfolio(self, image_list, horizontal):
        random.shuffle(image_list)
        list1 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (1200, 1200), (255, 255, 255))
        bg.paste(horizontal, (0, 0))
        for image in list1:
            if count == 1:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (0, 600))
            if count == 2:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (400, 600))
            if count == 3:
                image = image.resize((400, 600), Image.ANTIALIAS)
                bg.paste(image, (800, 600))
            count += 1
        timestr = ImageProcess.timestamp(self)
        filename = 'collage' + str(timestr) + '.jpg'
        filename = os.path.join(args.output, filename)
        if args.text:
            bg = ImageProcess.draw_text(self, bg, args.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)


if __name__ == "__main__":
    # Argument parsing
    parser = ArgumentParser(description='Automatic Photo Collage Maker.')
    parser.add_argument('-f', '--folder', dest='folder',
                        help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parser.add_argument('-o', '--output', dest='output',
                        help='path to the destination folder where images are to be saved')
    parser.add_argument('-t', '--text', dest='text', type=str, action='store',
                        help='text that you want to display on final collages')
    args = parser.parse_args()
    # create an instance of defined class
    process = CollageCreation()
    # Run according to whether path is a file or a directory

    if not args.folder:
        print('Input directory is not provided. Current directory will be choosen for input image. ')

    if not args.output:
        print('Output directory is not provided. New directory with time-stamp will be created.')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = 'collage' + timestr
        args.output = os.path.join(os.getcwd(), filename)
        os.makedirs(args.output)

    if not args.text:
        print('Text not provided. Collages without any text will be created.')

    if isfile(args.folder):
        print('Please provide different directory containing at-least 2 images.. ')
        exit(1)
    elif isdir(args.folder):
        count, images = process.processdir(args.folder)
        print('Number of Input Images: ' + str(count))

    # shuffle images if needed
    random.shuffle(images)
    # image_list = []
    # list_hor = []
    # list_ver = []
    horizontal = []
    vertical = []
    # for img in images:
    #     ar = img.size[0] / img.size[1]
    #     if(ar > 1):
    #         list_hor.append(img)
    #     else:
    #         list_ver.append(img)
    #     # image_list.append(img)

    # # random.shuffle(image_list)
    # print('Number of horizontal images: ', len(list_hor))
    # print('Number of vertical images: ', len(list_ver))

    for img in images:
        img.thumbnail((1800, 1800), Image.ANTIALIAS)
        ar = img.size[0] / img.size[1]
        if ar < 1:
            vertical.append(img)
            image1 = process.face_detection(img, 1200, 800)
            horizontal.append(image1)
        else:
            horizontal.append(img)
            image2 = process.face_detection(img, 800, 1200)
            vertical.append(image2)
    temp = images[0]
    temp = process.face_detection(img, 1200, 600)

    # print(len(vertical), len(horizontal))
    # if(len(list_hor) < 2):
    #     print('Please provide more than 2 horizontal images.')
    #     exit(1)

    # if (len(list_ver) < 4):
    #     print('Please provide more than 4 vertical images.')
    #     exit(1)

    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # images_directory = os.path.join(APP_ROOT, 'images')
    # thumbnails_directory = os.path.join(APP_ROOT, 'thumbnails')
    # collages_directory = os.path.join(APP_ROOT, 'collages')
    # data_directory = os.path.join(APP_ROOT, 'data')
    # fonts_directory = os.path.join(APP_ROOT, 'fonts')
    # print(APP_ROOT)
    # print(data_directory)
    # print(thumbnails_directory)
    # print(fonts_directory)

    # if(len(list_hor) > 2) and (len(list_ver) < 4):
    #     process.collage_2_hor(list_hor)
    #     process.collage_2_hor(list_hor)

    # if (len(list_hor) < 2) and (len(list_ver) > 4):
    #     process.collage_4(list_ver)
    #     process.black_magic(list_ver)
    #     process.collage_4(list_ver)
    #     process.black_magic(list_ver)

    # if (len(list_hor) > 2) and (len(list_ver) > 4):
    #     process.collage_3_hor(list_hor, list_ver)
    #     process.collage_3_hor(list_hor, list_ver)
    #     process.collage_4(list_ver)
    #     process.black_magic(list_ver)
    #     process.collage_4(list_ver)
    #     process.black_magic(list_ver)
    #     process.collage_2_hor(list_hor)
    #     process.collage_2_hor(list_hor)

    # process.collage_3_hor(horizontal, vertical)
    # process.collage_2_hor(horizontal)
    # process.collage_4(vertical)
    # process.black_magic(vertical)
    process.portfolio(vertical, temp)

    # process.collage_3_hor(horizontal, vertical)
    # process.collage_2_hor(horizontal)
    # process.collage_4(vertical)
    # process.black_magic(vertical)

    print('All collages has been created. Head over to the output directory...')
