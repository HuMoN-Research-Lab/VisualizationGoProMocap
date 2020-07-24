
import numpy as np, bpy
from mathutils import Matrix, Vector, Euler
from math import *
import time
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring, SubElement, Comment
from datetime import datetime
import xml.dom.minidom


#default number of frames to output is all of them - change this value to an integer if you 
#want to output less 
#set to "all" to output all frames
num_frames_output = "all"
num_frames_output = 1
#num_frames_output = 4064
#Change: the path of the npy file 
input_npy = "/Users/jackieallex/Downloads/markerless-reconstructed/input_npy_data_files/JSM3_6000frame_Filtered.npy"
#Change: the path of the folder you want to export xml file and png frames of animation to
output_frames_folder = "/Users/jackieallex/Downloads/markerless-reconstructed/output_xml"

# the array is saved in the file 
arr = np.load(input_npy) 

#3D array holding [[[x, y, z], [x, y, z]], [[x, y, z], [x, y, z]]] 
#an array of frames, where each frame is an array of points and each point is an array of floats (x, y, z)
  
#the first frame
markers_list = arr[0]

#names of markers 
name_arr = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
"LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee",
"LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
"RBigToe", "RSmallToe", "RHeel"]

#use to create bones based on:
order_of_markers = []

#-----------------------------------------------------------------------------------
# Log info to XML file
# create the file structure
data = Element('Data')

# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)
dt_object = datetime.fromtimestamp(timestamp)
date = SubElement(data, "timestamp")
date.text = str(dt_object)

frames = SubElement(data, 'frames')

def create_node(parent, name, text):
    child1 = SubElement(parent, name)
    child1.text = text
#-----------------------------------------------------------------------------------   

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
    if (name < 25):
        #get name from name array "name_arr"
        mt.name = name_arr[name]
    elif(name < 46):
        mt.name = "HandR"
    elif(name < 67):
        mt.name = "HandL"
    else:
        mt.name = "Ball"
    #add to order_of_markers to facilitate creating bones
    order_of_markers.append(mt)
    #increment index of name of empty in list
    name += 1
    #link empty to scene
    bpy.context.scene.collection.objects.link( mt )
    #set empty's location 
    mt.location = coord
    #set the display size of the empty
    mt.empty_display_size = 0.2
    #sanity check
    #print(coord)
    
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
    #set location of bone head
    new_bone.head =  empty1.location
    #set location of bone tail
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
#Set bones in front and show axis
armature_data.show_in_front = True
#True to show axis orientation of bones and false to hide it
armature_data.data.show_axes = False

#get armature object
def get_armature():
    for ob in bpy.data.objects:
        if ob.type == 'ARMATURE':
            armature = ob
            break
    return armature

armature = get_armature()
    
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

#a list of tuples where each element represents the info for one bone, and 
#the tuple contains the bone name, the marker of the head, and the marker of the tail
list_of_bones_order = [('bone0', order_of_markers[1], order_of_markers[0]),
        ('bone1', order_of_markers[1], order_of_markers[8]),
        ('bone2', order_of_markers[8], order_of_markers[12]),
        ('bone3', order_of_markers[12], order_of_markers[13]),
        ('bone4', order_of_markers[13], order_of_markers[14]),
        ('bone5', order_of_markers[14], order_of_markers[21]),
        ('bone6', order_of_markers[14], order_of_markers[19]),
        ('bone7', order_of_markers[19], order_of_markers[20]),
        ('bone8', order_of_markers[8], order_of_markers[9]),
        ('bone9', order_of_markers[9], order_of_markers[10]),
        ('bone10', order_of_markers[10], order_of_markers[11]),
        ('bone11', order_of_markers[11], order_of_markers[24]),
        ('bone12', order_of_markers[11], order_of_markers[22]),
        ('bone13', order_of_markers[22], order_of_markers[23]),
        ('bone14', order_of_markers[1], order_of_markers[5]),
        ('bone15', order_of_markers[5], order_of_markers[6]),
        ('bone16', order_of_markers[6], order_of_markers[7]),
        ('bone17', order_of_markers[1], order_of_markers[2]),
        ('bone18', order_of_markers[2], order_of_markers[3]),
        ('bone19', order_of_markers[3], order_of_markers[4]),
        ('bone20', order_of_markers[0], order_of_markers[16]),
        ('bone21', order_of_markers[16], order_of_markers[18]),
        ('bone22', order_of_markers[0], order_of_markers[15])]

#the rightEar is not aligning with the rest of the data 
#bone23 = add_child_bone('bone23', order_of_markers[15], order_of_markers[17])

#-----------------------------------------------------------------------------------
# Add hands
#bone structure by empties same for handL (left hand) and handR (right hand)_
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/raw/master/doc/media/keypoints_hand.png
#handL0: head = 0, tail = 1
#handL1: head = 1, tail = 2
#handL2: head = 2, tail = 3
#handL3: head = 3, tail = 4
#handL4: head = 0, tail = 5
#handL5: head = 5, tail = 6
#handL6: head = 6, tail = 7
#handL7: head = 7, tail = 8
#handL8: head = 0, tail = 9
#handL9: head = 9, tail = 10
#handL10: head = 10, tail = 11
#handL11: head = 11, tail = 12
#handL12: head = 0, tail = 13
#handL13: head = 13, tail = 14
#handL14 head = 14, tail = 15
#handL15: head = 15, tail = 16
#handL16: head = 0, tail = 17
#handL17: head = 17, tail = 18
#handL18: head = 18, tail = 19
#handL19: head = 19, tail = 20

#based on marker # from order_of_markers array add bones for hands:
#left hand is 46-66 so add 46 to original 
left_hand_offset = 46
left_hand = [('handL0', order_of_markers[0+left_hand_offset], order_of_markers[1+left_hand_offset]),
    ('handL1', order_of_markers[1+left_hand_offset], order_of_markers[2+left_hand_offset]),
    ('handL2', order_of_markers[2+left_hand_offset], order_of_markers[3+left_hand_offset]),
    ('handL3', order_of_markers[3+left_hand_offset], order_of_markers[4+left_hand_offset]),
    ('handL4', order_of_markers[0+left_hand_offset], order_of_markers[5+left_hand_offset]),
    ('handL5', order_of_markers[5+left_hand_offset], order_of_markers[6+left_hand_offset]),
    ('handL6', order_of_markers[6+left_hand_offset], order_of_markers[7+left_hand_offset]),
    ('handL7', order_of_markers[7+left_hand_offset], order_of_markers[8+left_hand_offset]),
    ('handL8', order_of_markers[0+left_hand_offset], order_of_markers[9+left_hand_offset]),
    ('handL9', order_of_markers[9+left_hand_offset], order_of_markers[10+left_hand_offset]),
    ('handL10', order_of_markers[10+left_hand_offset], order_of_markers[11+left_hand_offset]),
    ('handL11', order_of_markers[11+left_hand_offset], order_of_markers[12+left_hand_offset]),
    ('handL12', order_of_markers[0+left_hand_offset], order_of_markers[13+left_hand_offset]),
    ('handL13', order_of_markers[13+left_hand_offset], order_of_markers[14+left_hand_offset]),
    ('handL14', order_of_markers[14+left_hand_offset], order_of_markers[15+left_hand_offset]),
    ('handL15', order_of_markers[15+left_hand_offset], order_of_markers[16+left_hand_offset]),
    ('handL16', order_of_markers[0+left_hand_offset], order_of_markers[17+left_hand_offset]),
    ('handL17', order_of_markers[17+left_hand_offset], order_of_markers[18+left_hand_offset]),
    ('handL18', order_of_markers[18+left_hand_offset], order_of_markers[19+left_hand_offset]),
    ('handL19', order_of_markers[19+left_hand_offset], order_of_markers[20+left_hand_offset]),
    ('wristL', order_of_markers[0+left_hand_offset], order_of_markers[4])]
    
#right hand is #25-45 so add 25 to original
right_hand_offset = 25
right_hand = [('handR0', order_of_markers[0+right_hand_offset], order_of_markers[1+right_hand_offset]),
    ('handR1', order_of_markers[1+right_hand_offset], order_of_markers[2+right_hand_offset]),
    ('handR2', order_of_markers[2+right_hand_offset], order_of_markers[3+right_hand_offset]),
    ('handR3', order_of_markers[3+right_hand_offset], order_of_markers[4+right_hand_offset]),
    ('handR4', order_of_markers[0+right_hand_offset], order_of_markers[5+right_hand_offset]),
    ('handR5', order_of_markers[5+right_hand_offset], order_of_markers[6+right_hand_offset]),
    ('handR6', order_of_markers[6+right_hand_offset], order_of_markers[7+right_hand_offset]),
    ('handR7', order_of_markers[7+right_hand_offset], order_of_markers[8+right_hand_offset]),
    ('handR8', order_of_markers[0+right_hand_offset], order_of_markers[9+right_hand_offset]),
    ('handR9', order_of_markers[9+right_hand_offset], order_of_markers[10+right_hand_offset]),
    ('handR10', order_of_markers[10+right_hand_offset], order_of_markers[11+right_hand_offset]),
    ('handR11', order_of_markers[11+right_hand_offset], order_of_markers[12+right_hand_offset]),
    ('handR12', order_of_markers[0+right_hand_offset], order_of_markers[13+right_hand_offset]),
    ('handR13', order_of_markers[13+right_hand_offset], order_of_markers[14+right_hand_offset]),
    ('handR14', order_of_markers[14+right_hand_offset], order_of_markers[15+right_hand_offset]),
    ('handR15', order_of_markers[15+right_hand_offset], order_of_markers[16+right_hand_offset]),
    ('handR16', order_of_markers[0+right_hand_offset], order_of_markers[17+right_hand_offset]),
    ('handR17', order_of_markers[17+right_hand_offset], order_of_markers[18+right_hand_offset]),
    ('handR18', order_of_markers[18+right_hand_offset], order_of_markers[19+right_hand_offset]),
    ('handR19', order_of_markers[19+right_hand_offset], order_of_markers[20+right_hand_offset]),
    ('wristR', order_of_markers[0+right_hand_offset], order_of_markers[7])] #right wrist

#helper to create armature from list of tuples
def tuple_to_armature(bones):
    for bone_name, bone_head, bone_tail in bones:
        add_child_bone(bone_name, bone_head, bone_tail)
        
#create all bones for skeleton body and hands
tuple_to_armature(list_of_bones_order)
tuple_to_armature(left_hand)
tuple_to_armature(right_hand)

#-----------------------------------------------------------------------------------
#parent heads and tails to empties
#use bone constraints 
def parent_to_empties(bone_name, head, tail):
    #enter pose mode
    bpy.ops.object.posemode_toggle()
    marker = armature.data.bones[bone_name]
    #Set marker selected
    marker.select = True
    #Set marker active
    bpy.context.object.data.bones.active = marker
    bone = bpy.context.object.pose.bones[bone_name]
    #Copy Location Pose constraint: makes the bone's head follow the given empty
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bone.constraints["Copy Location"].target = head
    #Stretch To Pose constraint: makes the bone's tail follow the given empty
    #stretches the bones to reach the tail to that empty so head location is not affected
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone.constraints["Stretch To"].target = tail
    #exit pose mode
    bpy.ops.object.posemode_toggle()
    
#set parents of heads and tails for each bone 
def tuple_to_parented(bones):
    for bone_name, bone_head, bone_tail in bones:
        parent_to_empties(bone_name, bone_head, bone_tail)

tuple_to_parented(list_of_bones_order)
tuple_to_parented(left_hand)
tuple_to_parented(right_hand)
#-----------------------------------------------------------------------------------
# Animate! 
#find number of frames in animation
num_frames = len(arr) #500 frames at 120 fps

#change start frame of animation
bpy.context.scene.frame_start = 1
#change end frame of animation
bpy.context.scene.frame_end = num_frames


#create a new handler to change empty positions every frame
def my_handler(scene): 
    frames_seen = 0
    print("frame")
    print(scene.frame_current)
    #must be in pose mode to set keyframes
    bpy.ops.object.mode_set(mode='POSE')
    #keep track of current_marker
    current_marker = 0
    #find the current frame number
    frame = scene.frame_current
    #get the list of marker points from the current frame
    markers_list = arr[frame]
    #iterate through list of markers in this frame
    for col in markers_list:
        frame = scene.frame_current
        coord = Vector((float(col[0]), float(col[1]), float(col[2])))
        empty = order_of_markers[current_marker] 
        #change empty position : this is where the change in location every frame happens
        #line to test IK solver
        #if(empty.name != "RElbow"):
        empty.location = coord
        current_marker += 1 
                
#-----------------------------------------------------------------------------------
#script to create a mesh of the armature 
def CreateMesh():
    obj = get_armature()

    if obj == None:
        print( "No selection" )
    elif obj.type != 'ARMATURE':
        print( "Armature expected" )
    else:
        return processArmature( bpy.context, obj )

#Use armature to create base object
def armToMesh( arm ):
    name = arm.name + "_mesh"
    dataMesh = bpy.data.meshes.new( name + "Data" )
    mesh = bpy.data.objects.new( name, dataMesh )
    mesh.matrix_world = arm.matrix_world.copy()
    return mesh

#Make vertices and faces 
def boneGeometry( l1, l2, x, z, baseSize, l1Size, l2Size, base ):
    x1 = x  * baseSize * l1Size * 0.5
    z1 = z  * baseSize * l2Size * 0.5
    
    x2 = Vector( (0, 0, 0) )
    z2 = Vector( (0, 0, 0) )

    verts = [
        l1 - x1 + z1,
        l1 + x1 + z1,
        l1 - x1 - z1,
        l1 + x1 - z1,
        l2 - x2 + z2,
        l2 + x2 + z2,
        l2 - x2 - z2,
        l2 + x2 - z2
        ] 

    faces = [
        (base+3, base+1, base+0, base+2),
        (base+6, base+4, base+5, base+7),
        (base+4, base+0, base+1, base+5),
        (base+7, base+3, base+2, base+6),
        (base+5, base+1, base+3, base+7),
        (base+6, base+2, base+0, base+4)
        ]

    return verts, faces

#Process the armature, goes through its bones and creates the mesh
def processArmature(context, arm, genVertexGroups = True):
    print("processing armature {0}".format(arm.name))

    #Creates the mesh object
    meshObj = armToMesh( arm )
    context.collection.objects.link( meshObj )

    verts = []
    edges = []
    faces = []
    vertexGroups = {}

    bpy.ops.object.mode_set(mode='EDIT')

    try:
        #Goes through each bone
        for editBone in [b for b in arm.data.edit_bones if b.use_deform]:
            boneName = editBone.name
            print( boneName )
            poseBone = arm.pose.bones[boneName]

            #Gets edit bone informations
            editBoneHead = editBone.head
            editBoneTail = editBone.tail
            editBoneVector = editBoneTail - editBoneHead
            editBoneSize = editBoneVector.dot( editBoneVector )
            editBoneRoll = editBone.roll
            editBoneX = editBone.x_axis
            editBoneZ = editBone.z_axis
            editBoneHeadRadius = editBone.head_radius
            editBoneTailRadius = editBone.tail_radius

            #Creates the mesh data for the bone
            baseIndex = len(verts)
            baseSize = sqrt( editBoneSize )
            newVerts, newFaces = boneGeometry( editBoneHead, editBoneTail, editBoneX, editBoneZ, baseSize, editBoneHeadRadius, editBoneTailRadius, baseIndex )

            verts.extend( newVerts )
            faces.extend( newFaces )

            #Creates the weights for the vertex groups
            vertexGroups[boneName] = [(x, 1.0) for x in range(baseIndex, len(verts))]

        #Assigns the geometry to the mesh
        meshObj.data.from_pydata(verts, edges, faces)

    except:
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode='OBJECT')
    #Assigns the vertex groups
    if genVertexGroups:
        for name1, vertexGroup in vertexGroups.items():
            groupObject = meshObj.vertex_groups.new(name = name1)
            for (index, weight) in vertexGroup:
                groupObject.add([index], weight, 'REPLACE')

    #Creates the armature modifier
    modifier = meshObj.modifiers.new('ArmatureMod', 'ARMATURE')
    modifier.object = arm
    modifier.use_bone_envelopes = False
    modifier.use_vertex_groups = True

    meshObj.data.update()

    return meshObj

mesh_obob = CreateMesh()

#-----------------------------------------------------------------------------------
# Clean up the mesh by removing duplicate vertices, make sure all faces are quads, etc

checked = set()
for selected_object in bpy.data.objects:
    if selected_object.type != 'MESH':
        continue
    meshdata = selected_object.data
    if meshdata in checked:
        continue
    else:
        checked.add(meshdata)
    bpy.context.view_layer.objects.active = selected_object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.tris_convert_to_quads()
    bpy.ops.mesh.normals_make_consistent()
    bpy.ops.object.editmode_toggle()
#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)

#-----------------------------------------------------------------------------------
#add in balls
iter = 0
color = [".003", ".004", ".002"]
length = len(order_of_markers)
if length > 67:
    #Set edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    #Set bones in front and show axis
    armature_data.show_in_front = True
    #True to show axis orientation of bones and false to hide it
    armature_data.data.show_axes = False
    for index in range (67, 70):
        empty = order_of_markers[index]
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))
        sphere = bpy.context.selected_objects[0]
        sphere.parent = empty
        sphere.matrix_world.translation = empty.matrix_world.translation
        #size of sphere
        sphere.scale[0] = 0.5
        sphere.scale[1] = 0.5
        sphere.scale[2] = 0.5
        bpy.ops.object.mode_set(mode='OBJECT')
        for f in sphere.data.polygons:
            f.use_smooth = True
        mat = bpy.data.materials.get("Material" + color[iter])
        if sphere.data.materials:
            # assign to 1st material slot
            sphere.data.materials[0] = mat
        else:
            # no slots
            sphere.data.materials.append(mat)
        iter += 1
        

#add visible markers mesh
'''
for index in range(0, 67):
    empty = order_of_markers[index]
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))
    sphere = bpy.context.selected_objects[0]
    sphere.parent = empty
    sphere.matrix_world.translation = empty.matrix_world.translation
    #size of sphere
    sphere.scale[0] = 0.1
    sphere.scale[1] = 0.1
    sphere.scale[2] = 0.1
    mat = bpy.data.materials.get("Material-marker")
    if sphere.data.materials:
        # assign to 1st material slot
        sphere.data.materials[0] = mat
    else:
        # no slots
        sphere.data.materials.append(mat)
''' 
            
#-----------------------------------------------------------------------------------

#Set armature active
bpy.context.view_layer.objects.active = armature_data
#Set armature selected
armature_data.select_set(state=True)

#material assignment
ob = mesh_obob

# Get material
mat = bpy.data.materials.get("Material")
if mat is None:
    # create material
    print("mat was none")
    mat = bpy.data.materials.new(name="Material")

# Assign it to object
if ob.data.materials:
    # assign to 1st material slot
    ob.data.materials[0] = mat
else:
    # no slots
    ob.data.materials.append(mat)

#-----------------------------------------------------------------------------------
#function to register custom handler
bpy.app.handlers.frame_change_post.clear()
def register():
    bpy.app.handlers.frame_change_post.append(my_handler)
   
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
    
register()
#-----------------------------------------------------------------------------------
'''
Currently not correct view

#Adjust camera position / rotation
bpy.ops.object.posemode_toggle()
camera = bpy.data.objects["Camera"]
camera.location = Vector((0, 0, -60))
camera.rotation_mode = "QUATERNION"
camera.rotation_quaternion[0] = 0
camera.rotation_quaternion[1] = 20
camera.rotation_quaternion[2] = -20
camera.rotation_quaternion[3] = 0

'''

#-----------------------------------------------------------------------------------
#script to export animation as pngs and add info to XML file
print("Saving frames...")
scene = bpy.context.scene
#set the number of frames to output 
if num_frames_output is "all":
    num_frames_output = scene.frame_end + 1
else: 
    num_frames_output += 1
#iterate through all frames
for frame in range(0, num_frames_output):
    #specify file path to the folder you want to export to
    scene.render.filepath = output_frames_folder + "/frames/" + str(frame)
    scene.frame_set(frame)
    #render frame
    bpy.ops.render.render(write_still=True)
    #add information for each frame to XML file
    child0 = SubElement(frames, 'frame' + str(frame))
    child1 = SubElement(child0, 'markers')
    child2 = SubElement(child0, 'armature')
    current_marker = 0
    #Log XML for each marker from original npy data
    for col in markers_list:
        coord = Vector((float(col[0]), float(col[1]), float(col[2])))
        empty = order_of_markers[current_marker] 
        marker_node = SubElement(child1, empty.name)
        create_node(marker_node, "Location", str(coord))
        current_marker += 1
    #Log XML for each bone's location and rotation
    for bone in bpy.data.objects['Armature'].pose.bones:
        bone_node = SubElement(child2, bone.name)
        create_node(bone_node, "Location", str(bone.location))
        create_node(bone_node, "Rotation", str(bone.rotation_quaternion)) 

#-----------------------------------------------------------------------------------
# Write and close XML file
print("Writing XML...")
#raw XML file
mydata = ET.tostring(data, encoding="unicode")
myfile = open(output_frames_folder + "/output_data_raw.xml", "w")
myfile.write(mydata)
myfile.close() 

#formatted human-readable XML file
dom = xml.dom.minidom.parseString(mydata)
pretty_xml_as_string = dom.toprettyxml()
myfile2 = open(output_frames_folder + "/output_data_pretty.xml", "w")
myfile2.write(pretty_xml_as_string)
myfile2.close()

print("finished!")