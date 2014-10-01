#!/bin/bash

echo "1"
echo $1

echo "2"
echo $2
 
FILES=*.tim
for f in $FILES
do
  b=${f//.tim}
  echo $b
  rosrun stats_analisys fremen_graph.py $b $1 $2
done


