import bpy 
import os 
import sys 


#imdir = str(sys.argv[6]); 


in_dir = "/home/mro7/data/blend_set/"
lst = os.listdir(in_dir)


out_dir = "/home/mro7/data/blend_set/test.avi"


resx = 720; #1920 
resy = 480; #1080 
bpy.data.scenes["Scene"].render.resolution_x = resx 
bpy.data.scenes["Scene"].render.resolution_y = resy 
bpy.data.scenes["Scene"].render.resolution_percentage = 100 


# Filter file list by valid file types.
candidates = []
c = 0
for item in lst:
    #print(item)
    fileName, fileExtension = os.path.splitext(item)
    if fileExtension == ".ppm":
        candidates.append(item)
    


file = [{"name":i} for i in candidates]   
n = len(file) 
print(n) 

# create the sequencer data
bpy.context.scene.sequence_editor_create()

a = bpy.ops.sequencer.image_strip_add(directory = in_dir, files = file, channel=1, frame_start=0, frame_end=n-1) 


stripname=file[0].get("name"); 
bpy.data.scenes["Scene"].frame_end = n 
bpy.data.scenes["Scene"].render.image_settings.file_format = 'AVI_JPEG' 
bpy.data.scenes["Scene"].render.filepath = out_dir 
bpy.ops.render.render( animation=True ) 


# Diagnostic to check whether the images were loaded 
#stripname=file[0].get("name"); 
#print(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname]) 
#print(dir(bpy.data.scenes["Scene"].sequence_editor.sequences[stripname]))