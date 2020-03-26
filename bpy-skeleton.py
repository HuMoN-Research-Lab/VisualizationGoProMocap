import numpy as np
from mathutils import Matrix, Vector, Euler
import bpy

# the array is saved in the file 
arr = np.load(r"C:\Users\jacki\OneDrive\Desktop\markerless-reconstructed\output_3d.npy") 

#3D array holding [[[x, y, z], [x, y, z]], [[x, y, z], [x, y, z]]] 
#an array of frames, where each frame is an array of points and each point is an array of floats (x, y, z)
  
#the first frame, holds 25 markers
markers_list = arr[0]

#names of markers 
name_arr = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
"LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee",
"LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
"RBigToe", "RSmallToe", "RHeel", "Background"]

#use to create bones based on:
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_pose_25.png
order_of_markers = []

print(markers_list)

#Create empties at marker positions    
name = 0
# make sure project unity is correct for imported data
#Unsure of units
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in markers_list:
    # parse string float value into floats, create Vector, set empty position to Vector
    # multiply by .001 because original data is recorded in millimeters, but we want meters for this project
    coord = Vector((float(col[0]), float(col[1]), float(col[2])))
    bpy.ops.object.add(type='EMPTY', location=coord)  
    mt = bpy.context.active_object  
    #get name from name array "name_arr"
    mt.name = name_arr[name]
    #add to order_of_markers to facilitate creating bones
    order_of_markers.append(mt)
    #increment name of empty
    name += 1
    bpy.context.scene.collection.objects.link( mt )
    mt.location = coord
    mt.empty_display_size = 0.2
    #sanity check
    print(coord)
    
#-----------------------------------------------------------------------------------
#Create armature of skeleton if it is the 1st frame

#bone structure by empties
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_pose_25.png
#bone0: head = 0, tail = 1
#bone1: head = 1, tail = 8
#bone2: head = 8, tail = 12
#bone3: head = 12, tail = 13
#bone4: head = 13, tail = 14
#bone5: head = 14, tail = 21
#bone6: head = 14, tail = 19
#bone7: head = 19, tail = 20
#bone8: head = 8, tail = 9
#bone9: head = 9, tail = 10
#bone10: head = 10, tail = 11
#bone11: head = 11, tail = 24
#bone12: head = 11, tail = 22
#bone13: head = 22, tail = 23
#bone14: head = 1, tail = 5
#bone15: head = 5, tail = 6
#bone16: head = 6, tail = 7
#bone17: head = 1, tail = 2
#bone18: head = 2, tail = 3
#bone19: head = 3, tail = 4
#bone20: head = 0, tail = 16
#bone21: head = 16, tail = 18
#bone22: head = 0, tail = 15
#bone23: head = 15, tail = 17