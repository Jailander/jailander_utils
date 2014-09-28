#!/usr/bin/env python

import math
import rospy
import sys

from bson import json_util
import json
from datetime import datetime
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt


import std_msgs.msg
#from topological_navigation.topological_node import *
#from strands_navigation_msgs.msg import TopologicalNode
#from strands_navigation_msgs.msg import TopologicalMap
from strands_navigation_msgs.msg import NavStatistics


from ros_datacentre.message_store import MessageStoreProxy


def get_datetime(date_text):
    try:
        val = datetime.strptime(date_text, '%A, %B %d %Y, at %H:%M:%S hours')
    except ValueError:
        try:
            date = "2014 - %s" %date_text
            val = datetime.strptime(date, '%Y - %A, %B %d, at %H:%M:%S hours')
            
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return val


class NavStatGraph(object):
    
    def __init__(self, map_name, filename) :
        #print "loading file from map %s" %filename
        #self.lnodes = 
        stats, allsts = self.loadStats(map_name)
        self.export_data(filename, stats, allsts)


    def export_data(self, filename, stats, allsts):
        cross_hist0 = []
        cross_hist1 = []
        print 'number of edges: '+str(len(stats))
        for i in stats :
            ndata = len(i)
            edge = i[0]['edge']
            print 'edge: '+edge+' number of samples: '+str(ndata)
            print 'start time: '+str(i[0]['start'])
            print 'end time: '+str(i[ndata-1]['ended'])
            nod = i[ndata-1]['ended'].date() - i[0]['start'].date()
            print 'days: '+str(nod)
            cross_hist1.append(ndata)
            cross_hist0.append(edge)
            filenamedge = str(filename+'_'+edge+'.edge')
            fed = open(filenamedge, "w")
            for j in i :
                jsonarray = json.dumps(j, default=json_util.default)
                fed.write(jsonarray)
                s_output = "\n"
                fed.write(s_output)
            fed.close
            
        filenameall = str(filename+'_ALL.edge')
        fall = open(filenameall, "w")
        for j in allsts:
            jsonarray = json.dumps(j, default=json_util.default)
            fall.write(jsonarray)
            s_output = "\n"
            fall.write(s_output)
        fall.close


        hist=[]
        hist.append(cross_hist0)
        hist.append(cross_hist1)
        filename2 = str(filename+'_edges.info')
        fi = open(filename2, "w")
        for i in range(0, (len(hist[0])-1)):
            s_output = "%s %d\n" %(hist[0][i], hist[1][i])
            fi.write(s_output)
        fi.close


    def loadStats(self, map_name):

        #point_set=str(sys.argv[1])
        #map_name=str(sys.argv[3])
    
        #msg_store = MessageStoreProxy(database='g_four_s', collection='message_store')

        msg_store = MessageStoreProxy()
    
        query_meta = {}
        query_meta["pointset"] = map_name

        print ""

        message_list = msg_store.query(NavStatistics._type, {}, query_meta)
        available = len(message_list) > 0

        print available

        if available <= 0 :
            rospy.logerr("Desired pointset '"+map_name+"' not in datacentre")
            rospy.logerr("Available pointsets: "+str(available))
            raise Exception("Can't find waypoints.")
    
        else :
            stats = []
            edges_list = []
            
            for i in message_list:
                #edg = {}
                edge = i[0].origin+'_'+i[0].target
                if edge not in edges_list :
                    edges_list.append(edge)
                #dat = i[1]["inserted_at"]#datetime.strptime(i[0].date_started, "%A, %B %d, at %H:%M:%S hours")
                dat = get_datetime(i[0].date_started)
                epo = dat.strftime('%s')
                #Thursday, May 15, at 12:13:00 hours
                val = {}
                val['start'] = dat
                val['ended'] = get_datetime(i[0].date_finished)
                val['epoch'] = epo
                val['status'] = i[0].status
                val['time'] = i[0].operation_time
                val['edge'] = edge
                #edg["stat"] = val
                #stats.append(edg)
                stats.append(val)
            
            #stats = sorted(stats, key=itemgetter('edge'))
            stata =[]
            for l in edges_list:
#                print '\n'
#                print "statistics for edge:"                
#                print l
                statb = []
                for j in stats :
                    #if j['stat']['edge'] == l :
                    #    statb.append(j["stat"])
                    if j['edge'] == l :
                        statb.append(j)
                statb = sorted(statb, key=itemgetter('epoch'))
                stata.append(statb)
            
            stats = sorted(stats, key=itemgetter('epoch'))
            
            return stata, stats


if __name__ == '__main__':
    if len(sys.argv) < 3 :
        print "usage: map_export map_name output_file.edges"
        sys.exit(2)

    dataset_name=str(sys.argv[1])
    filename=str(sys.argv[2])
    rospy.init_node('nav_stats_exporter')
    server = NavStatGraph(dataset_name, filename)