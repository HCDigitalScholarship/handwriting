"""
A script that extract the xy coordinates from xml files of the folder lineStrokes and convert them into
cpikle file as a potential training dataset.
Majority of the codes comes from this wonderful github: https://github.com/hardmaru/write-rnn-tensorflow/blob/master/utils.py
"""
import os
import pickle
import random
import xml.etree.ElementTree as ET
import csv

import numpy as np

def process(data_dir, data_file):
    # create data file from raw xml files from iam handwriting source.

    # built the list of xml files
    filelist = []
    # set the data file directory
    rootDir = data_dir
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            filelist.append(dirName + "/" + fname)
    
    # build stroke database of every xml file
    strokes = []
    for i in range(len(filelist)):
        if (filelist[i].endswith('.xml')):
            print('Processing ' + filelist[i])
            strokes.append(
                convert_stroke_to_array(
                    getStroke(
                        filelist[i]
                    )
                )
            )
    fd = open(data_file, 'a').close()
    fd = open(data_file, 'wb')
    pickle.dump(strokes, fd, protocol=2)
    fd.close()

# function to read each individual xml file
def getStroke(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    result = []

    
    # otoro's normalization
    x_offset = 1e20
    y_offset = 1e20
    y_height = 0
    for i in range(1,4):
        x_offset = min(x_offset, float(root[0][i].attrib['x']))
        y_offset = min(y_offset, float(root[0][i].attrib['y']))
        y_height = min(y_height, float(root[0][i].attrib['y']))
    y_height -= y_offset
    x_offset -= 100
    y_offset -= 100
    
    # this will change correspondingly.
    for stroke in root[1].findall('Stroke'):
        points = []
        for point in stroke.findall('Point'):
            points.append([float(point.attrib['x']) - x_offset, float(point.attrib['y']) - y_offset ])
        points.append([0.0, 0.0]) # this marks the end of the stroke.
        result.append(points)
    return result

# the codes from Andy. This normalization is used by Google vision
# I will adjust it to work with our model.
def parse_dict(dict):

    class_name = dict["filename"]
    inkarray = dict["strokes"]
    stroke_lengths = [len(stroke[0]) for stroke in inkarray]
    total_points = sum(stroke_lengths)
    np_ink = np.zeros((total_points, 3), dtype=np.float32)
    current_t = 0
    for stroke in inkarray:
        for i in [0, 1]:
            np_ink[current_t:(current_t + len(stroke[0])), i] = stroke[i]
        current_t += len(stroke[0])
        np_ink[current_t - 1, 2] = 1  # stroke_end
    # Preprocessing.
    # 1. Size normalization.
    lower = np.min(np_ink[:, 0:2], axis=0)
    upper = np.max(np_ink[:, 0:2], axis=0)
    scale = upper - lower
    scale[scale == 0] = 1
    np_ink[:, 0:2] = (np_ink[:, 0:2] - lower) / scale
    # 2. Compute deltas.
    np_ink = np_ink[1:, 0:2] - np_ink[0:-1, 0:2]
    return np_ink, class_name

# converts a list of arrays into a 2d numpy int16 array
def convert_stroke_to_array(stroke):
    n_point = 0
    for i in range(len(stroke)):
        n_point += len(stroke[i])
    stroke_data = np.zeros((n_point, 3), dtype=np.int16)

    prev_x = 0
    prev_y = 0
    counter = 0

    for j in range(len(stroke)):
        for k in range(len(stroke[j])):
            stroke_data[counter, 0] = int(stroke[j][k][0]) - prev_x
            stroke_data[counter, 1] = int(stroke[j][k][1]) - prev_y
            prev_x = int(stroke[j][k][0])
            prev_y = int(stroke[j][k][1])
            stroke_data[counter, 2] = 0
            if (k == (len(stroke[j]) - 1)):
                stroke_data[counter, 2] = 1
            counter += 1
    return stroke_data

process("./lineStrokes","strokes_training_data.cpkl")