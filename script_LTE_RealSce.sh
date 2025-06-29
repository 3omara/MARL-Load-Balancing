#! /bin/bash

tcl_dir="./scratch/RealSce/tcls/"
mapfile -t tcl_files < <(ls "$tcl_dir")
tcl_files=("${tcl_files[@]/mob.tcl}")
for i in {1..250}
do

	mod_index=$(( i % ${#tcl_files[@]} ))
	tclFile="${tcl_files[$mod_index]}"

	echo "Using mobility file $tclFile"

	cp "$tcl_dir/$tclFile" "$tcl_dir/mob.tcl"
	./waf --run "scratch/RealSce/RealSce --RunNum=$(($i))"
done
