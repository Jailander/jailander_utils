#!/usr/bin/env python

from bson import json_util
import json
from datetime import datetime
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt
import sys

def load_file(inputfile) :

    print "openning %s" %inputfile 
    fin = open(inputfile, 'r')
    print "Done"

    edges = []
    line = fin.readline()
    while line:
        edge = json.loads(line, object_hook=json_util.object_hook)
        edges.append(edge)
        line = fin.readline()
    fin.close()    
    
    return edges

def create_files(edges, lepoch, uepoch):

    edge = edges[0]['edge']
    ned = len(edges)
    filename3 = str(edge+'.data')
    fdat = open(filename3, "w")
    filename4 = str(edge+'.tim')
    fti = open(filename4, "w")
    filename5 = str(edge+'.trav')
    ftr = open(filename5, "w")

    if lepoch == '-1' :
        lepoch = edges[0]['epoch']
        ilepoch = int(lepoch)
    else :
        dlepoch = datetime.strptime(lepoch, "%d-%m-%Y")
        ilepoch = int(dlepoch.strftime('%s'))
    
    if uepoch == '-1' :
        uepoch = edges[ned-1]['epoch']
        iuepoch = int(uepoch)
    else :
        duepoch = datetime.strptime(uepoch, "%d-%m-%Y")
        iuepoch = int(duepoch.strftime('%s'))


    last_epoch=0
    last_sepoch=0
    last_status=1
    for i in edges :
        epoch = i['epoch']
        iepoch = int(epoch)
        time = i['time']
        if iepoch >= ilepoch and iepoch <= iuepoch :
            if i['status'] == 'success' and time < 120 :
                status = 1
                if last_status == 1 or (iepoch-last_sepoch) > 60 :
                    s_output = "%s %f\n" %(epoch, time)
                    fti.write(s_output)
                    s_output = "%s %d\n" %(epoch, status)
                    ftr.write(s_output)
                    last_sepoch=iepoch
                last_epoch=0
            else :
                status = 0
                if last_status == 1 or (iepoch-last_epoch) > 60 :
                    s_output = "%s %d\n" %(epoch, status)
                    ftr.write(s_output)
                    last_epoch=iepoch
                last_sepoch=0
            s_output = "%s %f %d\n" %(epoch, time, status)
            fdat.write(s_output)
            last_status=status
    fdat.close
    fti.close
    ftr.close


if __name__ == '__main__':
    if len(sys.argv) < 4 :
        print "usage: insert_map input lower_lim_epoch upper_lim_epoch"
	sys.exit(2)

    filename=str(sys.argv[1])
    lepoch=str(sys.argv[2])
    uepoch=str(sys.argv[3])
    edges=load_file(filename)
    create_files(edges, lepoch, uepoch)