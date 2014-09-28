#!/usr/bin/env python

import glob

from bson import json_util
import json
from datetime import datetime
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt
import sys


def load_files(inputfiles) :

    edges = []
    for ifile in inputfiles :
        #print "openning %s" %ifile 
        fin = open(ifile, 'r')
        #print "Done"
    
        edge = []
        line = fin.readline()
        while line:
            edg = json.loads(line, object_hook=json_util.object_hook)
            edge.append(edg)
            line = fin.readline()
        fin.close()
        edges.append(edge)
        
    return edges


def get_date_hist(edge) :
    ndata = len(edge)
    startdt = edge[0]['start'].date()
    enddt = edge[ndata-1]['ended'].date()
    
    nod = edge[ndata-1]['ended'].date() - edge[0]['start'].date()
    
#    print 'start time: '+str(startdt)
#    print 'end time: '+str(enddt)
#    print 'days: '+str(nod)
    
    date_hist = []
    dates = []
    times = []
    successes = []
    fails  = []    
    
    for i in range (0, nod.days+1):
        tdt = startdt + timedelta(days=i)
        dates.append(tdt)
        times.append(0)
        successes.append(0)
        fails.append(0)

    for i in edge:
        edate = i['start'].date()
        dind = edate - startdt
        dind = dind.days
        times[dind] = times[dind] + 1
        if i['status'] == 'success' :
            successes[dind] = successes[dind] + 1
        if i['status'] == 'fatal' :
            fails[dind] = fails[dind] + 1
    
    date_hist.append(dates)
    date_hist.append(times)
    date_hist.append(successes)
    date_hist.append(fails)
    return date_hist
    #graph_edges(date_hist)
#    for j in dates:
#        print j
    
    #for i in edges :


def generate_histograms(edges) :
    
    histograms = []
    edge_names =[]
    date_hists =[]
    for edge in edges :
        edge_names.append(edge[0]['edge'])
        date_hist = get_date_hist(edge)
        date_hists.append(date_hist)
    
    histograms.append(edge_names)
    histograms.append(date_hists)
    return histograms


def graph_edges(hist, title):
    N = len(hist[0])
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.3       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, hist[1], width, color='b')
    rects2 = ax.bar(ind+width, hist[2], width, color='g')
    rects3 = ax.bar(ind+width+width, hist[3], width, color='r')
            
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Crosses')
    ax.set_title(title)
    ax.set_xticks(ind+width+width)
    ax.set_xticklabels(hist[0], rotation='vertical')
    
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('Total', 'Success', 'fails') )

    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom', rotation='vertical')
                    
    
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    ftitle = "%s.png"%title
    plt.savefig(ftitle)

def graph_histograms(histograms):
    count = 0
    #print histograms[0]
    for i in histograms[1]:
        graph_edges(i, histograms[0][count])
        count += 1


if __name__ == '__main__':
#    if len(sys.argv) < 2 :
#        print "usage: insert_map input_file.txt dataset_name map_name"
#	sys.exit(2)

    a=glob.glob('*.edge')
#    print a
    edges = load_files(a)
    histograms = generate_histograms(edges)
    graph_histograms(histograms)
#    print edges
#
#
#
#    filename=str(sys.argv[1])
#    edges=load_file(filename)
#    date_hist(edges)
    #plt.show()
#
