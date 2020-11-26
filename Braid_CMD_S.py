# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:22:34 2020

@author: jakub.kucera
"""

import numpy as np
#from IDP_databases import cnt_X, dc_X
#from mysql.connector import MySQLConnection, Error
#from python_mysql_dbconfig import read_db_config
from Braid_main_S import poc
#from default_var_dict import getBase
import time
import IDP_geometry
import os
      
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def baseBraid(varVal,CADfile,MD):
    lPath = os.path.dirname(os.path.abspath(__file__))
    st1 = time.time() 

    #MD = np.load(lPath+"\\catiafiles\\meshfiles\\"+MeshFile+"_nodes.npy")
    
    MS = varVal["mandrel_speed"]
    spoolsPhy = varVal['spools']
    rotax = 0.15 #travel per second (rad/s)
    #0.11 for braid comparison oscar
    
    #ammending the number of iterations required based on expected braid angles
    ratio2 = MS/rotax
    #spoolsWa =  max(8,int(0.8*ratio2))
    spoolsWa = varVal['spools'] #temporary troubleshooting
    print(spoolsWa)
       
    #find points on mandrel centreline
    datum, cdArr = IDP_geometry.centreline(MD)
    WW = 0
    noSQL = np.zeros([1,12])
    while WW < 2:
        YARN = 0
        #for each yarn
        while YARN < spoolsWa:
            #following function simulates positioning of a specific yarn on mandrel surface
            pocList = poc(MD,varVal,YARN,WW,spoolsWa,spoolsPhy,datum,cdArr,CADfile,rotax)
            #cnnB,crrB = cnt_X('NCC')  
            i = 0
            while i < np.size(pocList,0):
                #pocList decomposed for clarity of the script
                x = pocList[i,1]
                y = pocList[i,2]
                z = pocList[i,3]
                xN = pocList[i,4]
                yN = pocList[i,5]
                zN = pocList[i,6]               
                bAngle = pocList[i,7]
                pitch =  pocList[i,9]
                tt = pocList[i,8]   
                tempo = np.matrix([[YARN,x,y,z,xN,yN,zN,bAngle,pitch,pitch,tt,WW]])
                noSQL = np.concatenate((noSQL,tempo),axis=0)
                '''
                query = "INSERT INTO "+GENfile+"(YARN,x,y,z,bAngle,xN,yN,zN,pitch,iteration_time,warpORweft) VALUES("
                query +=str(YARN)+","+str(x)+","+str(y)+","+str(z)+","+str(bAngle)+","+str(xN)+","+str(yN)+","+str(zN)+","+str(pitch)+","+str(tt)+","+str(WW)+")"
                #print(query)
                crrB.execute(query)  
                '''
                i = i + 1
            #cnnB.commit()
            #dc_X('NCC',cnnB,crrB)
            YARN = YARN + 1
        WW = WW + 1
    
    tt = time.time() - st1
    '''
    cnnB,crrB = cnt_X('NCC')  
    print("Total braiding simulation time:--- %s seconds ---" % (bstt)) 
    query = "INSERT INTO BraidMain(simulation_time) VALUES("+str(bstt)+")"
    crrB.execute(query)
    cnnB.commit()
    dc_X('NCC',cnnB,crrB)  
    '''
    np.savetxt('braid_data.csv', noSQL, delimiter=',', fmt='%d')
    return(noSQL)

#varVal, varMin,varMax = getBase()
#varVal["guide_rad"] = 300
#CADfile = "IDP_spar_A270_JK"
#MeshFile = "IDP_spar_A270_N001"
#baseBraid(varVal,CADfile,MeshFile)

       
