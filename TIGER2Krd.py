import re
import arcpy


__author__ = 'liurl1221@gmail.com'

# split the point
def splitPoint(point):
    value = []
    value.append(float(point[:9])/1000000)
    value.append(float(point[9:])/1000000)
    return value

# read data from RT2 file and store in dictionary. RT2 file stored the turning point of the lines in RT1
# key: numbers start with 7;
# value: geo location
def readRT2toDic():
    f = open('*****/Tiger/rd_2ktiger/TX/TGR48001.RT2','r')
    RT2_dic = {}
    for line in f:
        line = line.strip()
        columns = line.split()
        tps = [];
        for index,col in enumerate(columns):
            if index == 1:
                key = col
            elif index > 2:
                turningPoint = col[:18]
                value = splitPoint(turningPoint) #split the turning point
                tps.append(value)
        RT2_dic[key] = tps
    return RT2_dic
    


# read data from RT1 file and store in an array. RT1 file stores the types, starting coordination, and ending coordination of lines
def readRT1toArray():
    # load RT2 to dictionary
    RT2_dic = readRT2toDic()
    
    f = open('*****/Tiger/rd_2ktiger/TX/TGR48001.RT1','r')
    feature_info = [];
    for line in f:
        line = line.strip()
        columns = line.split()
        linetype = line[55:58]
        startPoint = columns[-2]
        endPoint = columns[-1]
        ref = columns[1]    # number starts with 7

        #if road name starts with 'A'
        if(linetype[0]== 'A'):
            temp = [];

            # add start point
            a = splitPoint(startPoint)
            temp.append(a)

            # add turning points if turning points exist
            if(ref in RT2_dic):
                tps = RT2_dic[ref]
                temp += tps

            # add end point
            b = splitPoint(endPoint)
            temp.append(b)
            
            feature_info.append(temp)
    return feature_info


    
__author__ = 'zxy1219@gmail.com'

if __name__ == "__main__":

    # A list of features and coordinate pairs
    # A list that will hold each of the Polyline objects
    features = readRT1toArray()
    for feature in feature_info:
        # Create a Polyline object based on the array of points
        # Append to the list of Polyline objects
        features.append(
            arcpy.Polyline(
                arcpy.Array([arcpy.Point(*coords) for coords in feature])))

    # Persist a copy of the Polyline objects using CopyFeatures
    arcpy.CopyFeatures_management(features, "*****/Tiger/rd_2ktiger/TX/polylines2.shp")



