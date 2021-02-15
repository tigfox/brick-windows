#!/bin/bash

# we need to read the contents of the data directory, and then build graphs (and web pages?) for each rrd db
data_dir="/mnt/datadisk/temps/"
img_dir="/mnt/datadisk/img/"

# this will make some graphs from each rrd file in the dir
makeDirGraph () {
	directory=$1
	for file in `ls ${data_dir}${directory}/`
	do
		echo "${data_dir}${1}/${file}"
		if [[ "$file" == *".rrd" ]]; then
			echo "got an rrd"
			echo $file
			filename=$(basename $file .rrd)
			sensor=$1
			rrdtool graph ${data_dir}${directory}/${sensor}.png \
				-a PNG \
				--title "Temperature" \
				--vertical-label "Temp Celcius" \
				--lower-limit 15 \
				DEF:radio=${data_dir}${directory}/${file}:${sensor}:AVERAGE \
				COMMENT:"Updated `date '+%m/%d %H\:%M'`   " \
                                LINE1:radio#0000FF:"Sensor ${sensor} Temp In C"
			new_graph="${datadir}${directory}/${sensor}.png"
			echo $new_graph
			cp $new_graph $img_dir
		fi
	done
        return
}

cd ${data_dir}
for i in `ls $data_dir`
do
	echo "sending directory $i"
	new_graph="$(makeDirGraph $i)"
	# cp $new_graph $img_dir
done
