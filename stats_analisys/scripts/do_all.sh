#!/bin/bash

rm ./*.trav*
rm ./*.tim*
rm ./*.data
rm ./*.png

rosrun stats_analisys process_edges.py
rosrun stats_analisys dmur_files.sh
rosrun stats_analisys graph_files.sh

