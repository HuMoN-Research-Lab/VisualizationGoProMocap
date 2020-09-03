import numpy as np, bpy, csv
from mathutils import Matrix, Vector, Euler
from math import *

input_csv = r"/Users/jackieallex/Downloads/markerless-reconstructed/input_csv/CamE.csv"

header_end = 3

frame_start = 0;

marker_names_row = 1

print("here")

# Create 2D array "arr" to hold all 3D coordinate info of markers
#return an array containing all marker locations at given frame
def create_data_arr(frame):
    current_row = file[frame + header_end]
    cols, rows = (3, int((len(current_row) - 1) / 3))
    arr = [[None]*cols for _ in range(rows)]
    count = 0
    count_row = 0
    for x in range(1, len(current_row)):
        arr[count_row][count] = current_row[x]
        count += 1
        if (count == 3):
            count = 0
            count_row += 1
    return arr
 
#-----------------------------------------------------------------------------------
#open file and read marker animation data
with open(input_csv, "r") as csv_file:
    file = list(csv.reader(csv_file, delimiter=','))
    #the data from the starting frame
    frame = frame_start
    arr = create_data_arr(frame)

#-----------------------------------------------------------------------------------
#Create an array of marker names 
current_row = file[marker_names_row] 
name_arr = []
previous_name = ""
for index in range(1, len(current_row)):
    if current_row[index] != previous_name:
        name_arr.append(current_row[index])
        previous_name = current_row[index]
    

#-----------------------------------------------------------------------------------
#Create empties at marker positions    
name = 0
#an array to hold all marker objects
order_of_markers = []
# make sure project unit is correct for imported data
bpy.context.scene.unit_settings.length_unit = 'METERS'
#iterate through arr and create an empty object at that location for each element
for col in arr:
    # parse string float value into floats, create Vector, set empty position to Vector
    # multiply by .001 because original data is recorded in millimeters, but we want meters for this project
    coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, 0))
    bpy.ops.object.add(type='EMPTY', location=coord)  
    mt = bpy.context.active_object  
    #get name from name array "name_arr"
    mt.name = name_arr[name]
    #increment name of empty
    name += 1
    #link empty to this scene
    bpy.context.scene.collection.objects.link( mt )
    #set empty location
    mt.location = coord
    #set empty display size
    mt.empty_display_size = 0.1
    #add empty to array order_of_markers so we can later access it 
    order_of_markers.append(mt)
print(order_of_markers)


#-----------------------------------------------------------------------------------
#add visible sphere meshes on each marker

for empty in order_of_markers:
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))
    sphere = bpy.context.selected_objects[0]
    sphere.parent = empty
    sphere.matrix_world.translation = empty.matrix_world.translation
    #size of sphere
    sphere.scale[0] = 0.015
    sphere.scale[1] = 0.015
    sphere.scale[2] = 0.015
    mat = bpy.data.materials.get("Material-marker")
    if sphere.data.materials:
        # assign to 1st material slot
        sphere.data.materials[0] = mat
    else:
        # no slots
        sphere.data.materials.append(mat)

 
#-----------------------------------------------------------------------------------
#add visible sphere meshes on each marker

for empty in order_of_markers:
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, location=(0, 0, 0))
    sphere = bpy.context.selected_objects[0]
    sphere.parent = empty
    sphere.matrix_world.translation = empty.matrix_world.translation
    #size of sphere
    sphere.scale[0] = 0.015
    sphere.scale[1] = 0.015
    sphere.scale[2] = 0.015
    
#find number of frames in file
num_frames = len(file) - header_end

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = num_frames 
    
    
#handler function runs on every frame of the animation                
def my_handler(scene): 
    frames_seen = 0
    #keep track of current_marker
    current_marker = 0 
    #find the current frame number
    frame = scene.frame_current
    #get the list of marker points from the current frame
    markers_list = create_data_arr(frame)
    #iterate through list of markers in this frame
    for col in markers_list:
        if (col[0] and col[1] and col[2]):
            coord = Vector((float(col[0]) * 0.001, float(col[1]) * 0.001, 0)) # place the x, y, coordinates with z = 0
            empty = order_of_markers[current_marker] 
            #change empty position : this is where the change in location every frame happens
            empty.location = coord
            #Set keyframes of the empty location at this frame to save the animation
            #empty.keyframe_insert(data_path='location',frame=scene.frame_current)
            #increment counter of the number marker we are currently changing
        current_marker += 1 
    


#--------------------------------------------------------------------
#append handler function
                
bpy.app.handlers.frame_change_post.clear()
#function to register custom handler
def register():
   bpy.app.handlers.frame_change_post.append(my_handler)
   
def unregister():
    bpy.app.handlers.frame_change_post.remove(my_handler)
        
register()
