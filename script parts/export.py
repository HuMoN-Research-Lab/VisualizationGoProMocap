import bpy
import time

#script to export animation as pngs
scene = bpy.context.scene
for frame in range(scene.frame_start, scene.frame_end + 1):
    #specify file path to the folder you want to export to
    scene.render.filepath = "/Users/jackieallex/Downloads/markerless-reconstructed/frame/" + str(frame).zfill(4)
    scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    time.sleep(3)

print("finished!")