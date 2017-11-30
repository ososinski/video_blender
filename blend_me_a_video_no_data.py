#!/usr/bin/python3.4

import os
import bpy
import glob
import argparse
import numpy as np
from bpy import context
scene = context.scene

import sys
argv = sys.argv
argv = argv[argv.index("-P") + 1:]  # get all args after "--"
argv.remove("--")
sys.argv = argv
print(argv)  # --> ['example', 'args', '123']


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg
    #    return open(arg, 'r')  # return an open file #handle


parser = argparse.ArgumentParser(description='Plot data array [META_DATA] and [video] as an [OUT]<rubbish>.dvd @ 30fps using h264 encoding')
parser.add_argument('file', metavar="META_DATA", help='the file to process', type=lambda x: is_valid_file(parser, x))
parser.add_argument('--video', dest='video',default="vid/video.mov",
                    help='video file name', type=lambda x: is_valid_file(parser, x))
parser.add_argument('--out', dest='output',default="output",
                    help='output file name (default: video<rubbish>.dvd)')
parser.add_argument('--fps',  dest='fps',default=30, type=int,
                    help='input video frame_rate' )
parser.add_argument('--offset',  dest='offset', default=0.0, type=float,
                    help='video offset in seconds' )
parser.add_argument('-v', '--verbose', dest='DEBUG', action='store_true', default=False, help='Print stuff and save the blend file')
#parser.add_argument('--', dest='blender', action='store_true', default=False, help='running as blender script')

args = parser.parse_args()

path = os.path.dirname(os.path.realpath((args.file))) #"/home/mro7/data/blend_set/"
filename = os.path.basename(args.file) #"meta_data.dat"
vidpath = os.path.dirname(os.path.realpath((args.video))) #"vid/video.mov"
vidname = os.path.basename(args.video)

#options
resx = 540#720 #1920 
resy = 296 #480; #1080 
scene.render.fps = args.fps #30
scene.render.filepath = args.output #"video.avi"
DEBUG = args.DEBUG #True#False
video_offset = args.offset #10

# load in the metadata (wasteful, but reading all columns means we can add stuff to it)
meta_data = np.genfromtxt("%s/%s"%(path,filename), dtype=None, delimiter=' ', names=True)


# create the sequencer data
scene.sequence_editor_create()
#files = glob.glob("%s/frame*.png"%(path))
#files.sort()

#print(files)
#exit(0)

# set the movie strip / scale and offset

#load new movie clip
#bpy.data.movieclips.load("%s/%s"%(vidpath,vidname))
##get the new movie clip
#movie_clip = bpy.data.movieclips.get(vidname)
##assign movie clip to the node
##bpy.context.scene.node_tree.nodes['Movie Clip'].clip = movie_clip
#
#vid = scene.sequence_editor.sequences.new_clip(#movie(
#        name="video_clip",#os.path.basename(f),
#        #filepath = vidpath,
#        clip = movie_clip,
#        channel=1, frame_start=-video_offset*scene.render.fps)
#
#    #translation
#vid.blend_type = 'OVER_DROP'#'ADD'
##vid.use_translation = True
##vid.transform.offset_x = 720
##vid.transform.offset_y = 0
#
#### compute scale
#scale_x = (526)/(resx)#movie_clip.size[0]
#scale_y = (296)/(resy)#movie_clip.size[0]
#uniform_scale = (scale_x if (scale_x<scale_y) else scale_y)
#
##movie_clip = bpy.data.movieclips.get(os.path.basename(vidpath))
#
#
##print(movie_clip.size[0],movie_clip.size[1], uniform_scale)
##exit(1)
#
#scale = scene.sequence_editor.sequences.new_effect(
#        name="video_scale",
#        channel=2,
#        type = 'TRANSFORM',
#        frame_start = -video_offset*scene.render.fps,
#        seq1 = vid
#
#)
#scale.blend_type = 'ALPHA_OVER'
##scale.use_uniform_scale = True
#scale.scale_start_y = uniform_scale
#scale.scale_start_x = uniform_scale
#scale.use_translation = True
#scale.transform.offset_x = resx/4 #(half+30)/2
#scale.transform.offset_y = -((resy/4)+10)
#
#print(dir(vid))
#exit(1)


# set the frame/time counters
#seq = []
frame_origin = meta_data['timestamp'][0]-0.5
current_frame = 0
duration = 0
seq = None
sseq = None

for row in meta_data:
    filename = "frame%05d_comp.png"%row['image_number']
    statsname = "frame%05d_stats.png"%row['image_number']
    duration = (row['timestamp']-frame_origin)*scene.render.fps
    frame_origin = row['timestamp']

    #try:
    #    seq.frame_final_duration = duration #+ scene.render.fps
    #    sseq.frame_final_duration = duration #+ scene.render.fps
    #except:
    #    pass

    ### no if try hack
    try:
        seq.frame_final_end = current_frame #duration #+ scene.render.fps
    #    sseq.frame_final_end = current_frame #duration #+ scene.render.fps
    except:
        pass

    # image sequencer

    seq = scene.sequence_editor.sequences.new_image(
        name=filename,#os.path.basename(f),
        filepath=os.path.join(path, filename),
        channel=3, frame_start=current_frame)
    #seq.frame_final_duration = duration
    #current_frame = current_frame+duration
    if(DEBUG):
        print("%s @ %f s ~> %d frames"%(filename, duration/scene.render.fps, duration))
    
    #translation
    seq.blend_type = 'OVER_DROP'
    seq.use_translation = True
    seq.transform.offset_x = 0
    seq.transform.offset_y = 0

    # now stats sequencer sseq
    #sseq = scene.sequence_editor.sequences.new_image(
    #    name=statsname,#os.path.basename(f),
    #    filepath=os.path.join(path, statsname),
    #    channel=4, frame_start=current_frame)
    ##seq.frame_final_duration = duration
    # 
    ##translation
    #sseq.blend_type = 'OVER_DROP'
    #sseq.use_translation = True
    #sseq.transform.offset_x = 0
    #sseq.transform.offset_y = 298 # height of the stats
#
    ## post increment
    current_frame = current_frame+duration
#
#exit(0)
### fill duration till end of second ( blender wants that)
while(current_frame%scene.render.fps>=1):
    current_frame+=1

seq.frame_final_end = current_frame
#sseq.frame_final_end = current_frame


'''
for f in files:
    duration = 30

    seq = scene.sequence_editor.sequences.new_image(
        name=os.path.basename(f),
        filepath=f,# files[0],#os.path.join(path, files[0]),
        channel=1, frame_start=current_frame)
    seq.frame_final_duration = duration
    #seq.use_reverse_frames = False #no such thing as reverse order on 1 frame

    current_frame = current_frame+duration
'''
# add the rest of the images.
#for f in files:
#    print(f)
#    seq.elements.append(os.path.basename(f))



#render settings
scene.render.resolution_x = resx 
scene.render.resolution_y = resy 
scene.render.resolution_percentage = 100 
scene.render.use_sequencer = 1
scene.frame_start = 0
scene.frame_end = current_frame # ignores the last frame

#actual encoder
scene.render.image_settings.file_format = "FFMPEG" #'AVI_JPEG' 
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.audio_codec = 'NONE'
#scene.render.ffmpeg.video_bitrate = 24300
#scene.render.ffmpeg.audio_bitrate = 0 
#scene.render.ffmpeg.minrate = 0
#scene.render.ffmpeg.maxrate = 30000
#scene.render.ffmpeg.buffersize = 2147483647

#and render
data_context = {"blend_data": context.blend_data, "scene": scene, "area": context.area, "window": context.window, "region": context.region}
bpy.ops.render.render(data_context, animation=True)
#print(dir(context))

#debug save
if DEBUG: 
    bpy.ops.wm.save_as_mainfile(filepath="generated.blend")
