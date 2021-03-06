# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:22:34 2020

@author: jakub.kucera
"""

import numpy as np
from Braid_main_S import poc
import time
import IDP_geometry
import os
      
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def baseBraid(varVal,CADfile,MD):
    #This function iterates through all yarns simulated
    
    spoolsPhy = varVal['spools']
    rotax = 0.15 #travel per second (rad/s)
    spoolsWa = varVal['spools'] #temporary troubleshooting
    print(spoolsWa)
       
    #find points on mandrel centreline
    datum, cdArr = IDP_geometry.centreline(MD)
    WW = 0
    noSQL = np.zeros([1,10])
    #for each spool travel direction
    while WW < 2:
        YARN = 0
        #for each yarn
        while YARN < spoolsWa:
            #following function simulates positioning of a specific yarn on mandrel surface
            pocList = poc(MD,varVal,YARN,WW,spoolsWa,spoolsPhy,datum,cdArr,CADfile,rotax)
 
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
                #tt = pocList[i,8]   
                tempo = np.matrix([[YARN,x,y,z,xN,yN,zN,bAngle,pitch,WW]])
                noSQL = np.concatenate((noSQL,tempo),axis=0)

                i = i + 1

            YARN = YARN + 1
        WW = WW + 1
    #store data in CSV
    np.savetxt('braid_data.csv', noSQL, delimiter=',', fmt='%d')
    return(noSQL)

#varVal, varMin,varMax = getBase()
#varVal["guide_rad"] = 300
#CADfile = "IDP_spar_A270_JK"
#MeshFile = "IDP_spar_A270_N001"
#baseBraid(varVal,CADfile,MeshFile)

       
