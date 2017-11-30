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


parser = argparse.ArgumentParser(description='Plot data array [META_DATA] as an [OUT].png @ [width] px.')
parser.add_argument('file', metavar="META_DATA", help='the file to process', type=lambda x: is_valid_file(parser, x))
parser.add_argument('-o', '--out', dest='output',default="OUT",
                    help='output file name (default: [FILE_STEM].png)')
parser.add_argument('-n', '--number', dest='number',
                    help='frame number', default=0, type=int)
parser.add_argument('-s', '--scaling', dest='scaling', default="linear",
                    help='veusz colour scaling [linear]')
parser.add_argument('-e','--height', dest='height', type=int, default=220,
                    help='the png height [220]')
parser.add_argument('-w', '--width', dest='width', type=int, default=720,  help='the png width [720]')
parser.add_argument('-l', '--label', dest='label', type=None, default="variance",  help='the data label to use <mean|variance> %s(0) %s(1) default [variance] ')
parser.add_argument('-d', '--display', dest='display', action='store_true', default=False, help='Display the result')

args = parser.parse_args()
args.dpi = 100

args.path = os.path.dirname(os.path.realpath((args.file)))

if args.output is "OUT":
    stem,ext = os.path.splitext(args.file)
    args.output = "%s_plot.png"%(stem)
else:
    pass
    
#print (args)

embed = veusz.embed.Embedded("veusz")

page = embed.Root.Add("page")
page.width.val = "%.02fin"%(args.width/100.0)
page.height.val = "%.02fin"%(args.height/100.0)

graph0 = page.Add("graph", autoadd=False, Background__transparency=100)

# Add a label
title = page.Add('label', label=" %s "%args.label, yPos=0.95,
    alignHorz='centre', alignVert='top',
    Text__size="%dpt"%(args.height/10.0), Text__font="sans")

embed.ImportFileCSV(args.file, readrows=False, dsprefix='',
   delimiter=' ', dssuffix='', linked=False, encoding='utf_8', renames={"top_width":"width","left_track":"width(1)","right_track":"width(2)"})#"variance(0)":"variance0", "variance(1)":"variance1", "mean(0)":"mean0", "mean(1)":"mean1"})

### graph0

x_axis0 = graph0.Add("axis")
y_axis0 = graph0.Add("axis")

x_axis0.min.val = "auto"
x_axis0.max.val = "auto"

y_axis0.min.val = "auto"
y_axis0.max.val = "auto"

plot0 = graph0.Add('xy', marker='circle',markerSize='0',PlotLine__color='red', PlotLine__width = "0.03825in", MarkerFill__color='green', PlotLine__bezierJoin=True)

graph0.leftMargin.val = "0cm"
graph0.rightMargin.val = "0cm"
graph0.topMargin.val = "0cm"
graph0.bottomMargin.val = "0cm"

plot0.xData.val = "timestamp"#"image_number"
if((args.label == 'variance') or (args.label == 'mean')):
    plot0.yData.val = "%s(0)"%(args.label)
else:
    plot0.yData.val = "%s"%(args.label)   

x_axis0.MinorTicks.hide.val = True
x_axis0.MajorTicks.hide.val = True
#x_axis0.autoMirror.val = False #mirror line on the other side
x_axis0.Line.hide.val = True
x_axis0.autoRange.val = "exact"
x_axis0.mode.val = "labels"
#x_axis0.datascale.val = 1

y_axis0.MinorTicks.hide.val = True
y_axis0.MajorTicks.hide.val = True
#y_axis0.autoMirror.val = False #mirror line on the other side
y_axis0.Line.hide.val = True
y_axis0.autoRange.val = "+5%"
y_axis0.mode.val = "labels"

graph0.Border.hide.val = True


### plot1

plot1 = graph0.Add('xy', marker='circle',markerSize='0',PlotLine__color='blue', PlotLine__width = "0.03825in", MarkerFill__color='green', PlotLine__bezierJoin=True)

plot1.xData.val = "timestamp"#"image_number"
plot1.yData.val = "%s(1)"%(args.label)

### plot2

plot2 = graph0.Add('xy', marker='circle',markerSize='0',PlotLine__color='green', PlotLine__width = "0.03825in", MarkerFill__color='green',  PlotLine__bezierJoin=True)

plot2.xData.val = "timestamp"#"image_number"
plot2.yData.val = "%s(2)"%(args.label)

### Line and other

#if(args.number!=0):
line = graph0.Add("line", mode="length-angle", length=0.99, angle=-90, Line__width="0.03875in", yPos = 0)

#line.positioning.val="axes"
line.xPos.val=(embed.GetData("timestamp")[0][args.number-1]-embed.GetData("timestamp")[0][0])/(embed.GetData("timestamp")[0][-1]-embed.GetData("timestamp")[0][0]) #args.number*1.0/embed.GetData("image_number")[0].shape[0]

print(line.xPos.val)
#print(embed.GetDatasets())
#print(embed.GetData("image_number")[0].shape)


#embed.Export("poisson.pdf", backcolor="white")

embed.Export(
    #"poisson_{dpi:n}.png".format(dpi=args.dpi),
    args.output,
    backcolor="white",
    dpi=args.dpi,
    antialias=True
)

if(args.display):
    embed.WaitForClose()
else:
    embed.Close()
