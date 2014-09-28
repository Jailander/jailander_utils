#!/bin/bash

FILES=*.tim
for f in $FILES
do
  b=${f//.tim}
  echo $b
  rosrun stats_analisys fremen_graph.py $b
done


