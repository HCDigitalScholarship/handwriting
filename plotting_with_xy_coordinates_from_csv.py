import os
import sys
import csv
import matplotlib.pyplot as plt

# read the xy coordinates from the csv file and plot them using matplotlib
def plotting_xy_coordinates_from_csv(csvfile):
    lst_of_xcoordinates = [] # a list for x coordinates
    lst_of_ycoordinates = [] # a list for y coordinates
    with open(csvfile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                lst_of_xcoordinates.append(int(row['xcoordinate']))
                lst_of_ycoordinates.append(int(row['ycoordinate']))
            except:
                pass
    plt.plot(lst_of_xcoordinates, lst_of_ycoordinates, 'ro')
    plt.show()
    #print(lst_of_xcoordinates)
    #print(lst_of_ycoordinates)


plotting_xy_coordinates_from_csv("./sentence1.inkml.csv")
