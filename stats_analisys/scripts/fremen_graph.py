#!/usr/bin/env python
import glob
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import sys

def load_file(inputfile) :

    timfile = inputfile+'.tim'
    print "openning %s" %timfile
    ftim = open(timfile, 'r')
    print "Done"

    data_epoch = []
    data_tim   = []

    line = ftim.readline()
    while line:
        inf = line.split(' ',2)
        data_epoch.append(int(inf[0]))
        data_tim.append(float(inf[1]))
        line = ftim.readline()
    ftim.close()

    tim_data = []
    tim_data.append(data_epoch)
    tim_data.append(data_tim)

    ftimfile = inputfile+'.tim.ftim'
    print "openning %s" %ftimfile 
    ftim = open(ftimfile, 'r')
    print "Done"

    fdata_epoch = []
    fdata_tim   = []

    line = ftim.readline()
    while line:
        inf = line.split(' ',2)
        fdata_epoch.append(int(inf[0]))
        fdata_tim.append(float(inf[1]))
        line = ftim.readline()
    ftim.close()
   
    ftim_data = []
    ftim_data.append(fdata_epoch)
    ftim_data.append(fdata_tim)


    timfile = inputfile+'.trav'
    print "openning %s" %timfile
    ftim = open(timfile, 'r')
    print "Done"

    trdata_epoch = []
    trdata_tim   = []

    line = ftim.readline()
    while line:
        inf = line.split(' ',2)
        trdata_epoch.append(int(inf[0]))
        trdata_tim.append(int(inf[1]))
        line = ftim.readline()
    ftim.close()

    tra_data = []
    tra_data.append(trdata_epoch)
    tra_data.append(trdata_tim)


    ftimfile = inputfile+'.trav.ftrav'
    print "openning %s" %ftimfile 
    ftim = open(ftimfile, 'r')
    print "Done"

    ftrdata_epoch = []
    ftrdata_tim   = []

    line = ftim.readline()
    while line:
        inf = line.split(' ',2)
        ftrdata_epoch.append(int(inf[0]))
        ftrdata_tim.append(float(inf[1]))
        line = ftim.readline()
    ftim.close()
   
    ftra_data = []
    ftra_data.append(ftrdata_epoch)
    ftra_data.append(ftrdata_tim)


    print "ALL Done"

    graph_edges(tim_data, ftim_data, tra_data, ftra_data, inputfile)



def graph_edges(tdata, fdata, trdata, ftrdata, title):

    title1 = title+'_time'
    
    nnn = len(trdata[0])
    startofdata=datetime.fromtimestamp(trdata[0][0])
    endofdata=datetime.fromtimestamp(trdata[0][nnn-1])
    nod = endofdata.date() - startofdata.date()
    
    print startofdata,endofdata,nod.days
    print startofdata.strftime("%A %d. %B %Y"), startofdata.weekday()
    
    until_next_sunday = 6 - startofdata.weekday()
    first_sunday = startofdata+timedelta(days=until_next_sunday)      
    first_sunday = first_sunday.replace(hour=23, minute=59, second=59)
    firs_w_line = int(first_sunday.strftime('%s'))

    if startofdata.weekday() <= 4 :
        until_next_friday = 4 - startofdata.weekday()
        first_friday = startofdata+timedelta(days=until_next_friday)      
        first_friday = first_friday.replace(hour=23, minute=59, second=59)
        firs_we_line = int(first_friday.strftime('%s'))
    else :
        until_next_friday = 4 #- first_sunday.weekday()
        first_friday = first_sunday+timedelta(days=until_next_friday)      
        first_friday = first_friday.replace(hour=23, minute=59, second=59)
        firs_we_line = int(first_friday.strftime('%s'))
    
    startofdata = startofdata.replace(hour=23, minute=59, second=59)
    first_line = int(startofdata.strftime('%s'))
    
    
    fig = plt.figure(1)     # the first figure
    
    ax = fig.add_subplot(211)  # the first subplot in the first figure
    plt.plot(tdata[0], tdata[1], 'r', tdata[0], tdata[1], 'bx')
    plt.title(title1)
    
    a = ax.get_ylim()
    #print a[1]
    for i in range(firs_w_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], a, 'g--',  linewidth=0.7)
    
    for i in range(firs_we_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], a, 'y--',  linewidth=0.5)
        
    for i in range(first_line,trdata[0][nnn-1], 86400) :
        plt.plot([i, i], a, 'k--',  linewidth=0.05)

    #cc= ax.get_yaxis()
    #print cc.get_ylimit()
    
    fig = plt.figure(1)
    ax = fig.add_subplot(212)
    #rects1 = ax.plot(fdata[0], fdata[1], color='b')
    plt.plot(fdata[0], fdata[1], color='b')
    
    a = ax.get_ylim()
    for i in range(firs_w_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], a, 'g--',  linewidth=0.7)
    for i in range(firs_we_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], a, 'y--',  linewidth=0.5)
    for i in range(first_line,trdata[0][nnn-1], 86400) :
        plt.plot([i, i], a, 'k--',  linewidth=0.05)
    
    title1 = title1+'.png'
    plt.savefig(title1)    
    
    title2 = title+'_traversability'

    plt.figure(2)     # the first figure
    
    plt.subplot(211)  # the first subplot in the first figure

    for i in range(firs_w_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], [-0.1, 1.1], 'g--',  linewidth=0.7)
        
    for i in range(firs_we_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], [-0.1, 1.1], 'y--',  linewidth=0.5)
        
    for i in range(first_line,trdata[0][nnn-1], 86400) :
        plt.plot([i, i],[-0.1, 1.1], 'k--',  linewidth=0.05)
        
    plt.plot(trdata[0], trdata[1], 'r', trdata[0], trdata[1], 'bx')
    plt.ylim(-0.1, 1.1)
    plt.title(title2)    
    
    plt.figure(2)
    plt.subplot(212)

    for i in range(firs_w_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], [-0.1, 1.1], 'g--',  linewidth=0.7)

    for i in range(firs_we_line,trdata[0][nnn-1], 604800) :
        plt.plot([i, i], [-0.1, 1.1], 'y--',  linewidth=0.5)
        
    for i in range(first_line,trdata[0][nnn-1], 86400) :
        plt.plot([i, i], [-0.1, 1.1], 'k--',  linewidth=0.05)

    plt.plot(ftrdata[0], ftrdata[1], color='b')    
    plt.ylim(-0.1, 1.1)

    title2 = title2+'.png'   
    plt.savefig(title2)    
    #plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print "usage: insert_map input_file.txt dataset_name map_name"
	sys.exit(2)

    filename=str(sys.argv[1])
    #dataset_name=str(sys.argv[2])
    #map_name=str(sys.argv[3])
    load_file(filename)
