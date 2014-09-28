#!/bin/bash

FILES=./*.edge
for f in $FILES
do
  echo "Processing $f file..."
  rosrun stats_analisys edge_load.py $f -1 -1
  # take action on each file. $f store current file name
  # cat $f
done

FILES=./*.tim
for f in $FILES
do
  echo "Processing $f file..."
  rosrun dmurr dmurr-standalone $f -1 300 >> $f.ftim
  # take action on each file. $f store current file name
  # cat $f
done

FILES=./*.trav
for f in $FILES
do
  echo "Processing $f file..."
  rosrun dmurr dmurr-standalone $f -1 300 >> $f.ftrav
  # take action on each file. $f store current file name
  # cat $f
done

