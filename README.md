# VisualizationGoProMocap
Go pro motion capture data visualized through 3D animation using Blender and Python 


<p align="center">
 <img src="https://user-images.githubusercontent.com/44556715/78394718-20a0d700-75ba-11ea-9f36-b12090c42fdd.gif">
</p>

## Tools / requirements:
- Blender 2.8 
- npy file containing xyz data for each marker 

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
- Create a new Blender project
- In the script editor, open the script "bpy-skeleton-with-hands.py" (or "bpy-skeleton" for data without hands)
- In script, change file location of npy data to where it is on your local file system
- Run script, markers and a skeleton should appear in the 3D viewport
- Switch to the animation viewport, and hit play - keyframes should appear for each frame as the armature is animated 
- When all frames have been keyframed, pause the animation. 
- Go to object mode, select the armature and hit Object > Animation > Bake Action
- In script editor, open script create-mesh.py and click run script. A mesh of the armature should appear in the 3D viewport.
- Now, you can adjust lighting and cameras, and you are ready to export
    - Run the script export.py to export as frames to create video animation, or export as fbx to import into Unity
    
## How the scripts work:
- import data from npy file
- create empty objects at each point position
- create an armature object
- add bones to armature object with heads and tails at correct empty positions
- parent the heads and tails of bones to correct empty objects
- register a custom handler function that will adjust the position of each empty for every frame
- set keyframes of bones on every frame to save animation
- create mesh with vertex groups and parent to armature 
