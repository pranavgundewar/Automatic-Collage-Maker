# -*- coding: utf-8 -*-
"""
Project:    Automatic Collage Maker
Script:     Abstract derived class for collage creation
@author:    Pranav Gundewar
"""
# Importing Libraries
from PIL import Image
from image_process import ImageProcess
import random
import os


class CollageCreation(ImageProcess):
    """
    Abstract master class for collage creation using diferent layouts.
    """

    def __init__(self, output_dir, text):
        # self.extensions = ['.jpg', '.jpeg', '.png']
        ImageProcess.__init__(self)
        self.output = output_dir
        self.text = text
        # print(self.output, self.text)

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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'top right')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
        # bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
        # bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)

    def portfolio(self, image_list, horizontal):
        random.shuffle(image_list)
        list1 = image_list[:4]
        count = 1
        bg = Image.new('RGB', (1200, 1200), (255, 255, 255))
        horizontal = horizontal.resize((1200, 600), Image.ANTIALIAS)
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
        filename = os.path.join(self.output, filename)
        if self.text:
            bg = ImageProcess.draw_text(self, bg, self.text, 30, 'bottom left')
        bg = ImageProcess.put_logo(self, bg, 'HauteBook', 30, 'bottom right')
        bg.save(filename, quality=90, optimize=True)
