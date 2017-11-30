import veusz.embed
import numpy as np
import argparse
import os

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg
    #    return open(arg, 'r')  # return an open file #handle


parser = argparse.ArgumentParser(description='Plot data array [FILE] as an [OUT].png @ [dpi] dpi.')
parser.add_argument('file', metavar="FILE", help='the files to process', type=lambda x: is_valid_file(parser, x))
parser.add_argument('-o', '--out', dest='output',default="OUT",
                    help='output file name (default: [FILE_STEM].png)')
parser.add_argument('--cMap', dest='colourMap',default="grey",
                    help='veusz colourMap [grey]')
parser.add_argument('-s', '--scaling', dest='scaling',default="log",
                    help='veusz colour scaling [log]')
parser.add_argument('--crop', nargs=4, dest='bb', metavar="N",default=[0,0,0,0],
                    help='image boundary [left right top bottom]', type=int)
parser.add_argument('--range', nargs=2, dest='minmax', metavar="N",default=[0,0],
                    help='value range [MIN MAX]', type=float)
parser.add_argument('--dpi', dest='dpi', type=int, default=100,  help='the png dpi [100]')
parser.add_argument('-d', '--display', dest='display', action='store_true', default=False, help='Display the result')

args = parser.parse_args()

filename = args.file

args.path = os.path.dirname(os.path.realpath((args.file)))

if args.output is "OUT":
    stem,ext = os.path.splitext(args.file)
    args.output = "%s_plot.png"%(stem)
else:
    pass
    

#print (args)

#print (filename)

#data = np.loadtxt(open(args.file[0], "rb"),dtype=float, delimiter=' ')

data = np.genfromtxt(args.file,dtype=float,delimiter=" ")

#print data.shape

embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "%.02fin"%(data.shape[1]/10.0)
page.height.val = "%.02fin"%(data.shape[0]/10.0)

graph = page.Add("graph", autoadd=False)

x_axis = graph.Add("axis")
y_axis = graph.Add("axis")


# this stops intelligent axis extending
#embed.Set('x/autoExtend', False)
#embed.Set('x/autoExtendZero', False)


image_plot = graph.Add("image")

if(args.minmax[0]!=0 or args.minmax[1]!=0):
    image_plot.min.val=args.minmax[0]
    image_plot.max.val=args.minmax[1]

graph.leftMargin.val = "0cm"
graph.rightMargin.val = "0cm"
graph.topMargin.val = "0cm"
graph.bottomMargin.val = "0cm"

embed.ImportFile2D(args.file, "img_2d")

embed.SetData2D("img", data)

image_plot.colorScaling.val = args.scaling
image_plot.colorMap.val = args.colourMap


image_plot.data.val = "img_2d"


x_axis.MinorTicks.hide.val = True
x_axis.MajorTicks.hide.val = True
#x_axis.autoMirror.val = False #mirror line on the other side
x_axis.Line.hide.val = True
x_axis.autoRange.val = "exact"
x_axis.mode.val = "labels"
#x_axis.datascale.val = 1

y_axis.MinorTicks.hide.val = True
y_axis.MajorTicks.hide.val = True
#y_axis.autoMirror.val = False #mirror line on the other side
y_axis.Line.hide.val = True
y_axis.autoRange.val = "exact"
y_axis.mode.val = "labels"

graph.Border.hide.val = True

#resize for different crop // the 'if' because we all make top/bottom value mistakes
if(args.bb[0]!=0 or args.bb[1]!=0 or args.bb[2]!=0 or args.bb[3]!=0):
    page.width.val = "%fin"%(abs(args.bb[1]-args.bb[0])/10.0)
    if args.bb[0]<args.bb[1] :
        x_axis.min.val = args.bb[0]
        x_axis.max.val = args.bb[1]
    else:
        x_axis.min.val = args.bb[1]
        x_axis.max.val = args.bb[0]
    page.height.val = "%fin"%(abs(args.bb[3]-args.bb[2])/10.0)
    if args.bb[2]<args.bb[3] :
        y_axis.min.val = args.bb[2]
        y_axis.max.val = args.bb[3]
    else:
        y_axis.min.val = args.bb[3]
        y_axis.max.val = args.bb[2]


#typeface = "Arial"

#for curr_axis in [x_axis, y_axis]:
#    curr_axis.Label.font.val = typeface
#    curr_axis.TickLabels.font.val = typeface


#embed.Export("poisson.pdf", backcolor="white")

embed.Export(
    #"poisson_{dpi:n}.png".format(dpi=args.dpi),
    args.output,
    backcolor="white",
    dpi=args.dpi,
    antialias=False
)

if(args.display):
    embed.WaitForClose()
else:
    embed.Close()
