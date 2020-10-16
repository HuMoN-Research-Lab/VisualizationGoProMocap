import pickle, numpy as np, bpy
from mathutils import Matrix, Vector, Euler

infile = open(r"/Users/jackieallex/Downloads/markerless-reconstructed/input_pickle/camera_pos.pkl",'rb')
new_dict = pickle.load(infile)
infile.close()

infileCoords = open(r"/Users/jackieallex/Downloads/markerless-reconstructed/input_pickle/Charuco_3D_coords.pkl",'rb')
new_dict2 = pickle.load(infileCoords)
infileCoords.close()

print(new_dict.get('Calibration/1'))

def charucoMarkers():
    for x in new_dict2:
        # parse string float value into floats, create Vector, set empty position to Vector
        coord = Vector((float(x[0]), float(x[1]), float(x[2])))
        bpy.ops.object.add(type='EMPTY', location=coord)  
        mt = bpy.context.active_object  
        #link empty to scene
        bpy.context.scene.collection.objects.link( mt )
        #set empty's location 
        mt.location = coord
        #set the display size of the empty
        mt.empty_display_size = 0.2
    return mt
 
def rot2eul(R):
    beta = -np.arcsin(R[2,0])
    alpha = np.arctan2(R[2,1]/np.cos(beta),R[2,2]/np.cos(beta))
    gamma = np.arctan2(R[1,0]/np.cos(beta),R[0,0]/np.cos(beta))
    x = np.array((alpha, beta, gamma))
    return x


#import video as plane
bpy.ops.import_image.to_plane(files=[{"name":"GH020046.MP4", "name":"GH020046.MP4"}], directory="/Users/jackieallex/Downloads/markerless-reconstructed/Videos /")
for obj in bpy.context.scene.objects:
        if obj.name.startswith("GH020046"):
            planeE = obj
            
planes = []
planes.append(planeE)

bpy.context.view_layer.objects.active = planes[0]
planes[0].select_set(state=True)
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.object.editmode_toggle()
bpy.ops.transform.rotate(value=-3.1386, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


#planes: set at origin, set camera facing down with far plane exactly on the ground plane such that it overlaps video perfectly, then parent and then move and rotate camera

def rotateCamera(calibration):
    x = new_dict.get(calibration)
    coord = Vector((float(x[0][3]), float(x[1][3]), float(x[2][3])))
    bpy.ops.object.add(type='CAMERA', location=coord)
    
    bpy.ops.transform.resize(value=(7, 7, 7), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    
    
    rotation_euler = rot2eul(x.T)
    bpy.context.object.rotation_euler = rotation_euler
    bpy.context.object.rotation_mode = 'ZYX'

    
    planes[0].rotation_mode = 'ZYX'
    planes[0].location = coord 
    planes[0].rotation_euler = rotation_euler
    
    return coord

    
#Place empties at charuco marker positions 
last_marker = charucoMarkers()
        

rotateCamera('Calibration/1')
rotateCamera('Calibration/2')
rotateCamera('Calibration/3')
last_coord = rotateCamera('Calibration/4')


bpy.context.view_layer.objects.active = planes[0]
planes[0].select_set(state=True)
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
mesh = bpy.data.meshes.new("ray")  # add the new mesh
obj = bpy.data.objects.new("ray_object", mesh)
col = bpy.data.collections.get("Collection")
#link to Collection
col.objects.link(obj)
#set as active object
bpy.context.view_layer.objects.active = obj

obj.select_set(state=True)
bpy.context.view_layer.objects.active = obj
#Create mesh outline of skeleton parts
 # verts made with XYZ coords
print(last_coord)
print(last_marker.location)
verts = []
faces = []

verts.append(last_coord)
verts.append(last_marker.location)

edges = [(0, 1)]

#Create the mesh with the vertices and faces
obj.data.from_pydata(verts, edges, faces)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.view_layer.objects.active = obj
obj.select_set(state=True)
#Set origin of the plane to its median center
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

#Add screw modifier to make it thicker and visible in render
bpy.ops.object.modifier_add(type='SCREW')
bpy.context.object.modifiers["Screw"].angle = 0
bpy.context.object.modifiers["Screw"].steps = 2
bpy.context.object.modifiers["Screw"].render_steps = 2
bpy.context.object.modifiers["Screw"].screw_offset = 0.1
bpy.context.object.modifiers["Screw"].use_merge_vertices = True

# Get material
mat = bpy.data.materials.get("Ray_red")
if mat is None:
    # create material
    print("mat was none")
    mat = bpy.data.materials.new(name="Ray_red")

# Assign it to object
if obj.data.materials:
    # assign to 1st material slot
    obj.data.materials[0] = mat
else:
    # no slots
    obj.data.materials.append(mat)

#--------------------------------------------------------------------------


'''
bpy.ops.object.add(type='CAMERA', location=location)
    ob = bpy.context.object
    ob.name = 'CamFrom3x4PObj'
    cam = ob.data
    cam.name = 'CamFrom3x4P'

    # Lens
    cam.type = 'PERSP'
    cam.lens = f_in_mm 
    cam.lens_unit = 'MILLIMETERS'
    cam.sensor_width  = sensor_width_in_mm

'''

'''

print(new_dict.get('Calibration/1'))


#converting from matrix to properly rotated blender camera found here: https://blender.stackexchange.com/questions/40650/blender-camera-from-3x4-matrix?rq=1

    # Input: P 3x4 numpy matrix
    # Output: K, R, T such that P = K*[R | T], det(R) positive and K has positive diagonal
    #
    # Reference implementations: 
    #   - Oxford's visual geometry group matlab toolbox 
    #   - Scilab Image Processing toolbox
def KRT_from_P(P):
    N = 3
    H = P[:,0:N]  # if not numpy,  H = P.to_3x3()

    [K,R] = rf_rq(H)

    K /= K[-1,-1]

    # from http://ksimek.github.io/2012/08/14/decompose/
    # make the diagonal of K positive
    sg = numpy.diag(numpy.sign(numpy.diag(K)))

    K = K * sg
    R = sg * R
    # det(R) negative, just invert; the proj equation remains same:
    if (numpy.linalg.det(R) < 0):
       R = -R
    # C = -H\P[:,-1]
    C = numpy.linalg.lstsq(-H, P[:,-1])[0]
    T = -R*C
    return K, R, T

# RQ decomposition of a numpy matrix, using only libs that already come with
# blender by default
#
# Author: Ricardo Fabbri
# Reference implementations: 
#   Oxford's visual geometry group matlab toolbox 
#   Scilab Image Processing toolbox
#
# Input: 3x4 numpy matrix P
# Returns: numpy matrices r,q
def rf_rq(P):
    P = P.T
    # numpy only provides qr. Scipy has rq but doesn't ship with blender
    q, r = numpy.linalg.qr(P[ ::-1, ::-1], 'complete')
    q = q.T
    q = q[ ::-1, ::-1]
    r = r.T
    r = r[ ::-1, ::-1]

    if (numpy.linalg.det(q) < 0):
        r[:,0] *= -1
        q[0,:] *= -1
    return r, q

# Creates a blender camera consistent with a given 3x4 computer vision P matrix
# Run this in Object Mode
# scale: resolution scale percentage as in GUI, known a priori
# P: numpy 3x4
def get_blender_camera_from_3x4_P(P, scale):
    # get krt
    K, R_world2cv, T_world2cv = KRT_from_P(numpy.matrix(P))

    scene = bpy.context.scene
    sensor_width_in_mm = K[1,1]*K[0,2] / (K[0,0]*K[1,2])
    sensor_height_in_mm = 1  # doesn't matter
    resolution_x_in_px = K[0,2]*2  # principal point assumed at the center
    resolution_y_in_px = K[1,2]*2  # principal point assumed at the center

    s_u = resolution_x_in_px / sensor_width_in_mm
    s_v = resolution_y_in_px / sensor_height_in_mm
    # TODO include aspect ratio
    f_in_mm = K[0,0] / s_u
    # recover original resolution
    scene.render.resolution_x = resolution_x_in_px / scale
    scene.render.resolution_y = resolution_y_in_px / scale
    scene.render.resolution_percentage = scale * 100

    # Use this if the projection matrix follows the convention listed in my answer to
    # https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    R_bcam2cv = Matrix(
        ((1, 0,  0),
         (0, -1, 0),
         (0, 0, -1)))

    # Use this if the projection matrix follows the convention from e.g. the matlab calibration toolbox:
    # R_bcam2cv = Matrix(
    #     ((-1, 0,  0),
    #      (0, 1, 0),
    #      (0, 0, 1)))

    R_cv2world = R_world2cv.T
    rotation =  Matrix(R_cv2world.tolist()) * R_bcam2cv
    location = -R_cv2world * T_world2cv

    # create a new camera
    bpy.ops.object.add(
        type='CAMERA',
        location=location)
    ob = bpy.context.object
    ob.name = 'CamFrom3x4PObj'
    cam = ob.data
    cam.name = 'CamFrom3x4P'

    # Lens
    cam.type = 'PERSP'
    cam.lens = f_in_mm 
    cam.lens_unit = 'MILLIMETERS'
    cam.sensor_width  = sensor_width_in_mm
    ob.matrix_world = Matrix.Translation(location)*rotation.to_4x4()

    #     cam.shift_x = -0.05
    #     cam.shift_y = 0.1
    #     cam.clip_start = 10.0
    #     cam.clip_end = 250.0
    #     empty = bpy.data.objects.new('DofEmpty', None)
    #     empty.location = origin+Vector((0,10,0))
    #     cam.dof_object = empty

    # Display
    cam.show_name = True
    # Make this the current camera
    scene.camera = ob
    bpy.context.scene.update()

def test2():
    P = Matrix([
    [2. ,  0. , - 10. ,   282.  ],
    [0. ,- 3. , - 14. ,   417.  ],
    [0. ,  0. , - 1.  , - 18.   ]
    ])
    # This test P was constructed as k*[r | t] where
    #     k = [2 0 10; 0 3 14; 0 0 1]
    #     r = [1 0 0; 0 -1 0; 0 0 -1]
    #     t = [231 223 -18]
    # k, r, t = KRT_from_P(numpy.matrix(P))
    get_blender_camera_from_3x4_P(P, 1)
    
get_blender_camera_from_3x4_P(new_dict.get('Calibration/1'), 1)
'''