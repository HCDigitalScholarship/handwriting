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
import matplotlib.pyplot as plt

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

# the codes from Andy. This normalization is used by Google vision
# I will adjust it to work with our model.
def parse_dict(dict):
    if dict is None:
        return None
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
    #np_ink = np_ink[1:, 0:2] - np_ink[0:-1, 0:2]
    # plot out the xy coordinate here, it is just a test to see if it is consistent after normalization
    list_of_x_coordinates = []
    list_of_y_coordinates = []
    for i in range(len(np_ink)):
        list_of_x_coordinates.append(np_ink[i][0]) # x coordinate
        list_of_y_coordinates.append(np_ink[i][1]) # y coordinate
    plt.plot(list_of_x_coordinates, list_of_y_coordinates, 'ro')
    plt.show()
    return np_ink, class_name

def create_dictionary_from_xml(xml_file_name):
    try:
        dict = {}
        filename = os.path.basename(xml_file_name).split('.')[0]
        dict['filename'] = filename
        tree = ET.parse(xml_file_name)
        root = tree.getroot()
        strokes_list = []
        list_of_x_coordinates = []
        list_of_y_coordinates = []
        for i in range(len(root[1])):
            x_list = []
            y_list = []
            stroke = root[1][i]
            for coordinates in stroke:
                x_list.append(int(coordinates.attrib['x']))
                list_of_x_coordinates.append(int(coordinates.attrib['x']))
                y_list.append(int(coordinates.attrib['y']))
                list_of_y_coordinates.append(int(coordinates.attrib['y']))
            
            stroke_list = [x_list, y_list]
            strokes_list.append(stroke_list)
            dict['strokes'] = strokes_list
        #print(dict)
        # plot out the xy coordinate here
        plt.plot(list_of_x_coordinates, list_of_y_coordinates, 'ro')
        plt.show()
        return dict
    except:
        return None

# create the training data for the handwriting modeling. The file format is pickle file.
def create_the_training_data(data_dir, data_file):
    # built the list of xml files
    filelist = []
    # set the data file directory
    rootDir = data_dir
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            filelist.append(dirName + "/" + fname)
    #print(filelist)
    
    strokes = [] # a list of strokes in array
    for file in filelist:
        print("Processing ", file)
        the_strokes_filename_pair = parse_dict(create_dictionary_from_xml(file))
        if the_strokes_filename_pair is not None:
            arrays = the_strokes_filename_pair[0] # we only need the strokes array
            strokes.append(arrays)
    print(strokes)
    
    # dump the training data into a big pickle file.
    fd = open(data_file, 'a').close()
    fd = open(data_file, 'wb')
    pickle.dump(strokes, fd, protocol=2)
    fd.close()

#process("./lineStrokes","strokes_training_data.cpkl")
create_the_training_data("./lineStrokes", "strokes_training_data.cpkl")