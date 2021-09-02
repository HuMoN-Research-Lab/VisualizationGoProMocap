# VisualizationGoProMocap
Go pro motion capture data visualized through 3D animation using Blender and Python 

<p align="center">
 <img src="https://user-images.githubusercontent.com/44556715/88416228-daac9080-cdad-11ea-8c7f-54f5d6586dea.gif">
</p>

<p align="center">
 <img src="https://user-images.githubusercontent.com/44556715/80505213-08ff0900-8942-11ea-87af-654d58b9355d.gif">
</p>

## Tools / requirements:
1. Blender 2.8 
2. npy file containing xyz data for each marker 

Data imported from npy file with format:
3D array holding [[[x, y, z], [x, y, z], ...], [[x, y, z], [x, y, z], ...], ...]  
- an array of frames, where each frame is an array of points and each point is an array of floats [x, y, z]
  
Each frame contains 25 or 67 points:
All frames contain:
```python
#names of markers 
name_arr = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder",
"LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee",
"LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
"RBigToe", "RSmallToe", "RHeel", "Background"]
```
If the skeleton from the data has hands, then the frame will have 67 points where:
- 1-25 : same as above
- 26-46 : right hand 
- 47-67 : left hand

## Steps for set-up:
1. Open Blender project starter file for desired lighting/material & camera, or start with a new Blender 3D project
2. In the script editor, open the script "npy-to-frames.py" (requires data with hands, use "bpy-skeleton.py" for data without hands)
3. In script, change file location of npy data to where it is on your local file system
4. Change the file location of the output folder to be where you want the frames and XML data output to save to
5. Run script
6. This will export the frames of the full animation of the npy file from the view of the camera in 3D space with a 3D skeleton 

## How the scripts work:
1. import data from npy file
2. create empty objects at each point position
3. create an armature object
4. add bones to armature object with heads and tails at correct empty positions
5. parent the heads and tails of bones to correct empty objects
6. register a custom handler function that will adjust the position of each empty for every frame
7. set keyframes of bones' location and rotation on every frame to save animation
8. create mesh with vertex groups and parent to armature 
9. assign material to mesh
10. Export png frames
11. Export XML data for each frame 
