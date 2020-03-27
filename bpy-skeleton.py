import numpy as np
from mathutils import Matrix, Vector, Euler
import bpy

# the array is saved in the file 
arr = np.load(r"/Users/jackieallex/Downloads/markerless-reconstructed/output_3d.npy") 

#3D array holding [[[x, y, z], [x, y, z]], [[x, y, z], [x, y, z]]] 
#an array of frames, where each frame is an array of points and each point is an array of floats (x, y, z)
  
#the first frame, holds 25 markers
markers_list = arr[0]

#names of markers 
name_arr = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
"LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee",
"LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
"RBigToe", "RSmallToe", "RHeel"]

#use to create bones based on:
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_pose_25.png
order_of_markers = []

print(markers_list)

#Create empties at marker positions    
name = 0
# make sure project unit is correct for imported data
#Unsure of units
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in markers_list:
    # parse string float value into floats, create Vector, set empty position to Vector
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

#adds child bone given corresponding parent and empty
#bone tail will appear at the location of empty
def add_child_bone(bone_name, empty1, empty2):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,0.5,0)
    #Set bone's location to wheel
    new_bone.matrix = empty2.matrix_world
    new_bone.head =  empty1.location
    new_bone.tail = empty2.location
    return new_bone

#Create armature object
armature = bpy.data.armatures.new('Armature')
armature_object = bpy.data.objects.new('Armature', armature)
#Link armature object to our scene
bpy.context.collection.objects.link(armature_object)
#Make armature variable
armature_data = bpy.data.objects[armature_object.name]
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)
#Set edit mode
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#Set bones In front and show axis
armature_data.show_in_front = True
armature_data.data.show_axes = True

#Add root bone
bone0 = armature_data.data.edit_bones.new('bone0')
#Set its orientation and size
bone0.head = (0,0,0)
bone0.tail = (0,0.5,0)
#Set its location 
bone0.tail = order_of_markers[0].location
bone0.head =  order_of_markers[1].location

#get armature object
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        armature = ob
        break
    
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

#Add wheel bones to armature
bone1 = add_child_bone('bone1', order_of_markers[1], order_of_markers[8])
bone2 = add_child_bone('bone2', order_of_markers[8], order_of_markers[12])
bone3 = add_child_bone('bone3', order_of_markers[12], order_of_markers[13])
bone4 = add_child_bone('bone4', order_of_markers[13], order_of_markers[14])
bone5 = add_child_bone('bone5', order_of_markers[14], order_of_markers[21])
bone6 = add_child_bone('bone6', order_of_markers[14], order_of_markers[19])
bone7 = add_child_bone('bone7', order_of_markers[19], order_of_markers[20])
bone8 = add_child_bone('bone8', order_of_markers[8], order_of_markers[9])
bone9 = add_child_bone('bone9', order_of_markers[9], order_of_markers[10])
bone10 = add_child_bone('bone10', order_of_markers[10], order_of_markers[11])
bone11 = add_child_bone('bone11', order_of_markers[11], order_of_markers[24])
bone12 = add_child_bone('bone12', order_of_markers[11], order_of_markers[22])
bone13 = add_child_bone('bone13', order_of_markers[22], order_of_markers[23])
bone14 = add_child_bone('bone14', order_of_markers[1], order_of_markers[5])
bone15 = add_child_bone('bone15', order_of_markers[5], order_of_markers[6])
bone16 = add_child_bone('bone16', order_of_markers[6], order_of_markers[7])
bone17 = add_child_bone('bone17', order_of_markers[1], order_of_markers[2])
bone18 = add_child_bone('bone18', order_of_markers[2], order_of_markers[3])
bone19 = add_child_bone('bone19', order_of_markers[3], order_of_markers[4])
bone20 = add_child_bone('bone20', order_of_markers[0], order_of_markers[16])
bone21 = add_child_bone('bone21', order_of_markers[16], order_of_markers[18])
bone22 = add_child_bone('bone22', order_of_markers[0], order_of_markers[15])
bone23 = add_child_bone('bone23', order_of_markers[15], order_of_markers[17])


#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    bpy.ops.object.posemode_toggle()
    #Armature name is "Armature.004"
    marker = armature.data.bones[bone_name]
    #Set marker selected
    marker.select = True
    #Set marker active
    bpy.context.object.data.bones.active = marker
    bone = bpy.context.object.pose.bones[bone_name]
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bone.constraints["Copy Location"].target = head
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone.constraints["Stretch To"].target = tail
    bpy.ops.object.posemode_toggle()
    
#set parents of heads and tails for each bone 
parent_to_empties('bone1', order_of_markers[1], order_of_markers[8])
parent_to_empties('bone2', order_of_markers[8], order_of_markers[12])
parent_to_empties('bone3', order_of_markers[12], order_of_markers[13])
parent_to_empties('bone4', order_of_markers[13], order_of_markers[14])
parent_to_empties('bone5', order_of_markers[14], order_of_markers[21])
parent_to_empties('bone6', order_of_markers[14], order_of_markers[19])
parent_to_empties('bone7', order_of_markers[19], order_of_markers[20])
parent_to_empties('bone8', order_of_markers[8], order_of_markers[9])
parent_to_empties('bone9', order_of_markers[9], order_of_markers[10])
parent_to_empties('bone10', order_of_markers[10], order_of_markers[11])
parent_to_empties('bone11', order_of_markers[11], order_of_markers[24])
parent_to_empties('bone12', order_of_markers[11], order_of_markers[22])
parent_to_empties('bone13', order_of_markers[22], order_of_markers[23])
parent_to_empties('bone14', order_of_markers[1], order_of_markers[5])
parent_to_empties('bone15', order_of_markers[5], order_of_markers[6])
parent_to_empties('bone16', order_of_markers[6], order_of_markers[7])
parent_to_empties('bone17', order_of_markers[1], order_of_markers[2])
parent_to_empties('bone18', order_of_markers[2], order_of_markers[3])
parent_to_empties('bone19', order_of_markers[3], order_of_markers[4])
parent_to_empties('bone20', order_of_markers[0], order_of_markers[16])
parent_to_empties('bone21', order_of_markers[16], order_of_markers[18])
parent_to_empties('bone22', order_of_markers[0], order_of_markers[15])
parent_to_empties('bone23', order_of_markers[15], order_of_markers[17])

#-----------------------------------------------------------------------------------
# Animate!
#find number of frames in animation
num_frames = len(arr) #500 frames
    
#create a new handler to change empty positions every frame
def my_handler(scene):
    arr = np.load(r"/Users/jackieallex/Downloads/markerless-reconstructed/output_3d.npy") 
    bpy.ops.object.select_all(action='DESELECT')
    #keep track of current_marker
    current_marker = 0
    frame = scene.frame_current
    markers_list = arr[frame]
    for col in markers_list:
        coord = Vector((float(col[0]), float(col[1]), float(col[2])))
        empty = order_of_markers[current_marker]
        #Set empty active
        bpy.context.view_layer.objects.active = empty
        #Set empty selected
        empty.select_set(state=True)
        #change empty position
        empty.location = coord
        current_marker += 1

        
    #val = scene.objects['Cube'].location.x
    #scene.objects['Sphere'].location.y = val + 1.6
    
    
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)

#unregister handler
#def unregister():
    #bpy.app.handlers.frame_change_post.remove(my_handler)
    
    #once frame number hits max, unregister
    #read data from each frame 
    #starting after frame 0, change position of empties on each frame 
    #persistent handler?
    #test
    
register()