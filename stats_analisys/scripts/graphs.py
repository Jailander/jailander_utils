#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

def load_file(inputfile) :

    print "openning %s" %inputfile 
    fin = open(inputfile, 'r')
    print "Done"

    cross_hist0 = []
    cross_hist1 = []

    line = fin.readline()
    while line:
        inf = line.split(' ',2)
        cross_hist0.append(inf[0])
        cross_hist1.append(int(inf[1]))
        line = fin.readline()
    fin.close()

    hist=[]
    hist.append(cross_hist0)
    hist.append(cross_hist1)
    graph_edges(hist)
    
def graph_edges(hist):
    N = len(hist[0])
    #menMeans = (20, 35, 30, 35, 27)
    #menStd =   (2, 3, 4, 1, 2)
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.7       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, hist[1], width, color='r')
            
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Crosses')
    ax.set_title('Crosses by edge')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(hist[0], rotation='vertical')
    
    #ax.legend(rects1[0], 'crosses')
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
    autolabel(rects1)
    
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print "usage: insert_map input_file.txt dataset_name map_name"
	sys.exit(2)

    filename=str(sys.argv[1])
    #dataset_name=str(sys.argv[2])
    #map_name=str(sys.argv[3])

    load_file(filename)