# -*- coding: utf-8 -*-
"""
Project: Automatic Collage Maker
Program by :
@author    : Pranav Gundewar
"""
# Importing Libraries
from argparse import ArgumentParser
from image_process import ImageProcess
from collage_create import CollageCreation
import os
import random
from PIL import Image, ImageDraw, ImageFont
from os.path import isfile, isdir
from sys import exit
# from PIL.ExifTags import TAGS
import time
# import numpy as np
# import cv2

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
    # create an instance of defined class
    process = CollageCreation(args.output, args.text)

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

    # random.shuffle(image_list)

    for img in images:
        img.thumbnail((1200, 1200), Image.ANTIALIAS)
        ar = img.size[0] / img.size[1]
        if ar < 1:
            vertical.append(img)
            image1 = process.face_detection(img, 900, 600)
            horizontal.append(image1)
        else:
            horizontal.append(img)
            image2 = process.face_detection(img, 600, 900)
            vertical.append(image2)
    # shuffle images if needed
    random.shuffle(images)
    temp = images[0]
    temp = process.face_detection(img, 900, 450)

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

    process.collage_3_hor(horizontal, vertical)
    process.collage_2_hor(horizontal)
    process.collage_4(vertical)
    process.black_magic(vertical)
    process.portfolio(vertical, temp)

    # res = process.make_collage(images, 1200, 450)
    # if not res:
    #     print('Failed to create collage!')
    #     exit(1)
    res = process.make_collage(images, 800, 300)
    if not res:
        print('Failed to create collage!')
        exit(1)

    # process.collage_3_hor(horizontal, vertical)
    # process.collage_2_hor(horizontal)
    # process.collage_4(vertical)
    # process.black_magic(vertical)

    print('All collages has been created. Head over to the output directory...')
