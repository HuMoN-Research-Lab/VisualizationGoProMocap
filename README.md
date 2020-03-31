# VisualizationGoProMocap
Go pro motion capture data visualized through 3D animation using Blender and Python 

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

## Steps:
- import data from npy file
- create empty objects at each point position
- create an armature object
- add bones to armature object with heads and tails at correct empty positions
- parent the heads and tails of bones to correct empty objects
- register a custom handler function that will adjust the position of each empty for every frame
- set keyframes of bones on every frame to save animation
- bake animation pose data 
- change framerate of project to fit the animation
- correct the orientation and unit 
- after running script, press play to run the animation in the project -> as the frame # increases, the keyframes of the animation will be set.
- create a camera and render animation as png frames to create video or export as fbx to import into Unity

