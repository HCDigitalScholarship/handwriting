import os
import sys
import csv

# extracting xy-coordinates from a inkxml file and write it into a new text file
def extraction_of_xy_coordinate_from_xml(xml_file_name):
    # a list to record the xy coordinates
    lst_of_xycoordinates = []
    label_of_the_sentence = "The sentence is "
    # open the xml file
    with open(xml_file_name, 'r') as xmlFile:
        # skip to line 33 because we assume that the beginning 32 lines are not what we need
        for i in xrange(32):
            xmlFile.readline()
        # label of the sentence is at line 33
        label_tmp = xmlFile.readline().split("<label>")[1]
        label_of_the_sentence += label_tmp.split("</label>")[0]
        
        xmlFile.readline()
        # starts at line 35
        tmp = xmlFile.readline()
        while tmp != "":
            try:
                # processing the split by comma of line 35
                string_split = tmp.split(',')
                length_of_string_split = len(string_split)
            
                # get the first and last xy-coordinates
                tmpstr = string_split[0].split(' ')
                first_xycoordinates = tmpstr[-2] + " " + tmpstr[-1]
                lst_of_xycoordinates.append(first_xycoordinates)

                # now processing the rest of the xy-coordinates
                for i in range(1,length_of_string_split-1):
                    lst_of_xycoordinates.append(string_split[i])

                # now processing the last xy-coordinates
                tmpstr1 = string_split[-1].split('<')
                last_xycoordinates = tmpstr1[0]
                lst_of_xycoordinates.append(last_xycoordinates)
                lst_of_xycoordinates.append("stroke stroke")
            except:
                pass
            tmp = xmlFile.readline()

    # create a new text file to record all the xy coordinates from the xml file
    new_file = xml_file_name + '.csv'
    open(new_file, 'a').close()
    """with open(new_file, 'a') as xy_coordinates_csv:
        xy_coordinates_csv.write("xcoordinate,ycoordinate")
        # we don't want the last two things in the list because they are </traceGroup> and </ink>
        for i in range(len(lst_of_xycoordinates)-2):
            xy_coordinates_csv.write(lst_of_xycoordinates[i])"""
    with open(new_file, 'w') as xy_coordinates_csv:
        fieldnames = ['xcoordinate', 'ycoordinate']
        writer = csv.DictWriter(xy_coordinates_csv, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(lst_of_xycoordinates)-3):
            tmp_str = lst_of_xycoordinates[i].split(' ')
            if len(tmp_str) == 2:
                writer.writerow({'xcoordinate':tmp_str[0] ,'ycoordinate':tmp_str[1]})
            elif len(tmp_str) == 3:
                writer.writerow({'xcoordinate':tmp_str[1] ,'ycoordinate':tmp_str[2]})
    with open(new_file, 'a') as xy_coordinates_append:
        xy_coordinates_append.write(label_of_the_sentence)

# iterate through a single directory.
def xy_coordinates_extraction(directory):
    # iterate through the inkml files inside the directory
    for file in os.listdir(directory):
        if file.endswith('.inkml'):
            extraction_of_xy_coordinate_from_xml(os.path.join(directory, file))
    # create a new directory to store the xycoordinates text files.
    if not os.path.exists(directory + "XYCoordinates"):
        os.makedirs(directory + "XYCoordinates")
    new_directory = directory + "XYCoordinates"
    # move the xycoordinates text files in to a new directory
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            os.rename(os.path.join(directory, file), os.path.join(new_directory, file))

# iterate through multiple directories in ImadocSen-OnDB/data/sentences
def iteration_of_directories(headDirectory):
    for directory in os.listdir(headDirectory):
        if directory != ".DS_Store":
            xy_coordinates_extraction(os.path.join(headDirectory,directory))

extraction_of_xy_coordinate_from_xml("./ImadocSen-OnDB/data/sentences/writer1d/sentence1.inkml")
#iteration_of_directories("./ImadocSen-OnDB/data/sentences/")