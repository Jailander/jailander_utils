#!/usr/bin/env python
import math
import rospy
import sys
from datetime import datetime
from operator import itemgetter

import std_msgs.msg
#from topological_navigation.topological_node import *
#from strands_navigation_msgs.msg import TopologicalNode
#from strands_navigation_msgs.msg import TopologicalMap
from strands_navigation_msgs.msg import NavStatistics


from ros_datacentre.message_store import MessageStoreProxy



class NavStatGraph(object):
    
    def __init__(self, map_name, filename) :
        #print "loading file from map %s" %filename
        #self.lnodes = 
        stats = self.loadStats(map_name)
        self.export_data(filename, stats)


    def export_data(self, filename, stats):
        
        for i in stats :
            ndata = len(i)
            edge = i[0]['edge']
            min_tm = i[0]['epoch']
            max_tm = i[ndata-1]['epoch']
            #Clean the file in case it existed
            filename2 = str(filename+'_'+edge+'.info')
            #print edge+'\t'+str(ndata)+'\t'+min_tm+'\t'+max_tm+'\t'
            fi = open(filename2, "w")
            s_output = "edge: \t%s\n" %edge
            fi.write(s_output)
            s_output = "Starting_time: \t%s\n" %min_tm
            fi.write(s_output)
            s_output = "Final_time: \t%s\n" %max_tm
            fi.write(s_output)
            window = int(max_tm)-int(min_tm)
            s_output = "Window: \t%d\n" %window
            fi.write(s_output)
            s_output = "Samples: \t%s\n" %ndata
            fi.write(s_output)
            fi.close
            filename3 = str(filename+'_'+edge+'.data')
            fdat = open(filename3, "w")
            filename4 = str(filename+'_'+edge+'.tim')
            fti = open(filename4, "w")
            filename5 = str(filename+'_'+edge+'.trav')
            ftr = open(filename5, "w")
            for j in i:
                epoch = j['epoch']
                time = j['time']
                if j['status'] == 'success' :
                    status = 1
                else :
                    status = 0
                s_output = "%s %f %d\n" %(epoch, time, status)
                fdat.write(s_output)
                s_output = "%s %d\n" %(epoch, status)
                ftr.write(s_output)
                s_output = "%s %f\n" %(epoch, time)
                fti.write(s_output)
            fdat.close
            fti.close
            ftr.close
                    
#    
#        #Write File
#        for i in self.lnodes :
#            fh = open(filename, "a")
#            print "node: \n\t%s" %i.name
#            s_output = "node: \n\t%s\n" %i.name
#            fh.write(s_output)
#            print "\twaypoint:\n\t%s" %i.waypoint
#            s_output = "\twaypoint:\n\t\t%f,%f,%f,%f,%f,%f,%f\n" %(float(i.waypoint[0]),float(i.waypoint[1]),float(i.waypoint[2]),float(i.waypoint[3]),float(i.waypoint[4]),float(i.waypoint[5]),float(i.waypoint[6]))
#            fh.write(s_output)
#            print "\tedges:"
#            s_output = "\tedges:\n"
#            fh.write(s_output)
#            for k in i.edges :
#                print "\t\t %s, %s" %(k['node'],k['action'])
#                s_output = "\t\t %s, %s\n" %(k['node'],k['action'])
#                fh.write(s_output)
#            print "\tvertices:"
#            s_output = "\tvertices:\n"
#            fh.write(s_output)
#            for k in i.vertices :
#                print "\t\t%f,%f" %(k[0],k[1])
#                s_output = "\t\t%f,%f\n" %(k[0],k[1])
#                fh.write(s_output)
#        fh.close


    def loadStats(self, map_name):

        #point_set=str(sys.argv[1])
        #map_name=str(sys.argv[3])
    
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
                edg = {}
                edge = i[0].origin+'_'+i[0].target
                if edge not in edges_list :
                    edges_list.append(edge)
                dat = i[1]["inserted_at"]#datetime.strptime(i[0].date_started, "%A, %B %d, at %H:%M:%S hours")
                epo = dat.strftime('%s')
                #Thursday, May 15, at 12:13:00 hours
                val = {}
                val['epoch'] = epo
                val['status'] = i[0].status
                val['time'] = i[0].operation_time
                val['edge'] = edge
                edg["stat"] = val
                stats.append(edg)
            
            #stats = sorted(stats, key=itemgetter('edge'))
            stata =[]
            for l in edges_list:
#                print '\n'
#                print "statistics for edge:"                
#                print l
                statb = []
                for j in stats :
                    if j['stat']['edge'] == l :
                        statb.append(j["stat"])
                statb = sorted(statb, key=itemgetter('epoch'))
                stata.append(statb)
            
            return stata           


if __name__ == '__main__':
    if len(sys.argv) < 3 :
        print "usage: map_export map_name output_file.edges"
        sys.exit(2)

    dataset_name=str(sys.argv[1])
    filename=str(sys.argv[2])
    rospy.init_node('nav_stats_exporter')
    server = NavStatGraph(dataset_name, filename)