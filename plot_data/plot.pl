#! /usr/bin/perl
use File::Glob;

foreach my $dir (@ARGV){
   if (!-d $dir){
      print ") '$dir' is not a valid directory\n";
   }else{
      my @files = glob("$dir/frame*.dat");
      foreach my $file (@files){
         my $plot = $file;
         $plot =~ s/\.dat/_plot.png/ig;
         print "> plotting $file\n";
         print "python veusz_plot_mahalanobis.py --out $plot --cMap 'seq' --scaling 'log' --dpi 10 --range 0.1 200 --crop 0 540 0 148 $file \n";
         my @error = `python veusz_plot_mahalanobis.py --out $plot --cMap 'seq' --scaling 'log' --dpi 10 --range 0.1 200 --crop 0 540 0 148 $file`;
         print "> with errors:\n@error\n" if(@error);
         print "> saved as $plot \n\n";
# generate variance graph
         my $variance = $file;
         $variance =~ s/\.dat/_variance.png/ig;
         $file =~ /frame0+(\d+).dat/g;
         my $frame_number = $1; 
         print "> plotting $file\n";
         print "python veusz_plot_metadata.py $dir/meta_data.dat --out $variance --number $frame_number  --width=1080 --height=100 --label variance \n";
         @error = `python veusz_plot_metadata.py $dir/meta_data.dat --out $variance --number $frame_number --width=1080 --height=100 --label variance`;
         print "> with errors:\n@error\n" if(@error);
         print "> saved as $variance \n\n";

# generate mean graph
         my $mean = $file;
         $mean =~ s/\.dat/_mean.png/ig;
         print "> plotting $file\n";
         print "python veusz_plot_metadata.py $dir/meta_data.dat --out $mean --number $frame_number  --width=1080 --height=100 --label mean \n";
         @error = `python veusz_plot_metadata.py $dir/meta_data.dat --out $mean --number $frame_number --width=1080 --height=100 --label mean`;
         print "> with errors:\n@error\n" if(@error);
         print "> saved as $mean \n\n";


# generate width graph
         my $width = $file;
         $width =~ s/\.dat/_width.png/ig;
         print "> plotting $file\n";
         print "python veusz_plot_metadata_same_axis.py $dir/meta_data.dat --out $width --number $frame_number  --width=1080 --height=100 --label width (+left+right) \n";
         @error = `python veusz_plot_metadata_same_axis.py $dir/meta_data.dat --out $width --number $frame_number --width=1080 --height=100 --label width`;
         print "> with errors:\n@error\n" if(@error);
         print "> saved as $width \n\n";


#The combination thingy
         my $frame = $file;
         $frame =~ s/\.dat//ig;
#crop and resize
         my $cmd = "convert ${frame}.ppm -crop 540x148+0+0  ${frame}_crop.png ";
         print "executing: $cmd\n";
         my $out = `$cmd`;
         print "$out";
         $cmd = "convert ${frame}_crop.png -filter Box -resize 540x ${frame}_crop.png ";
         print "executing: $cmd\n";
         $out = `$cmd`;
         print "$out";
         
#combine road and mahalanobis
	 $cmd = "convert -append ${frame}_crop.png $plot ${frame}_comp.png";
         print "executing: $cmd\n\n";
         $out = `$cmd`;
         print "$out";

#add a black line to variance
	 $cmd = "convert $variance -set page 1080x105 -background Black -flatten ${frame}_stats.png";
         print "executing: $cmd\n\n";
         $out = `$cmd`;
         print "$out";

#add a black line to mean
	 $cmd = "convert $mean -set page 1080x105 -background Black -flatten ${mean}";
         print "executing: $cmd\n\n";
         $out = `$cmd`;
         print "$out";

#combine variance and mean
	 $cmd = "convert -append ${frame}_stats.png $mean $width ${frame}_stats.png";
         print "executing: $cmd\n\n";
         $out = `$cmd`;
         print "$out";

      }
   }
}


#convert llan.ppm -filter Box -resize 720x compc.png
#convert llan.ppm -crop 180x55+0+0 compc.png
