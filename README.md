# video_blender

# [DESCRIPTION]

Scripts to create automated videos from meta-data [timestamp:image_name] and linking an existing video

Keep in mind it is a video processor so usually uses peak 1GB or ram, requires h264 library to be on the syste to compress the videos. Optional [in-code] uncompressed for the people with infinite hard drives.

Also includes automater plotter for Veusz (application specific one + label specific one, but easily modifiable by example)
To generate a video you will need to run:

# [USAGE]

#optional data plotter
plot_data/plot.pl <META_DATA_DIR>/

# video blender
./run_blender <META_DATA_DIR>/meta_data.dat --offset <VIDEO_OFFSET_IN_S> --fps <VIDEO_FPS> --out <ANYTHING> --video <VIDEO_FILE>

you need to specify your video's fps as there is no easy way to do it in blender

# [FAQ/EXAMPLE]

The example [meta_data.dat] file is included


# [DEPENDENCIES]
plotter : Veusz,imagemagick

video_blender: Blender
