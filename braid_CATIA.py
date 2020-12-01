# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:13:55 2020

@author: jakub.kucera
"""
from mesh_anyshape import cat_mesh
from Braid_CMD_S import baseBraid
import win32com.client.dynamic
import numpy as np
import time
import os


#takes in a CATIA file and creates MD mesh input for braiding
# 1.shape needs to start at z=0
# 2.the shape need centreline starting at x=0,y=0
# 3.all geometries need to be hidden
# 4.the complete surface needs to be called "MainLoft"

def b_master(part,varVal,vis):
    #Inputs are the CATIA file and "varVal"(collection of braiding parameters.
    #vis is binary visualisation parameter
    #Catia file includes path.
    
    #parameters passed into meshing algorithm
    mesh = varVal["mesh_size"]
    span = varVal["span"]
    spws = int(120/mesh) #the cross-section number of elements 
    ML = cat_mesh(span,part,spws,mesh)
    
    #the core braiding simulation
    noSQL = baseBraid(varVal,part,ML)
    
    
    #The rest of this script is for display
    if vis == True:
        #Open and setup CATIA file
        st42 = time.time() 
        CATIA = win32com.client.Dispatch("CATIA.Application")
        CATIA.RefreshDisplay = False 
        partDocument1 = CATIA.Documents.Open(part)
        part1 = partDocument1.Part
        HSF = part1.HybridShapeFactory
        hbs = part1.HybridBodies    
        #initial values
        BP = []
        yarn = 0
        ww = 0 
        count = 0
        hb2 = hbs.Add()
        hb2.Name="yarn"+str(yarn)
        x = 0
        y = 0
        z = 0
        #loop through all datapoints
        for row in noSQL:
            #maximum number of spools displayed is set to 20
            if count < 20:
                BP.append(row)
                yr = int(row[0,0])
                #reset yarn count for oposite direction
                if ww < row[0,9]:
                    yarn = 0
                    hb2 = hbs.Add()
                    hb2.Name="yarn_"+str(yarn)+"_direction_"+str(row[0,9])         
                ww = (row[0,9])
                if yarn < yr:
                    #data point corresponds to new yarn number
                    if yarn > 0:
                        count = count + 1
                        print(count)
                    yarn = yr
                    hb2 = hbs.Add()
                    hb2.Name="yarn_"+str(yarn)+"_direction_"+str(ww)
                
                #check for duplicate points, only plot non-duplicate
                diff = ((row[0,1]-x)**2+(row[0,2]-y)**2+(row[0,3]-z)**2)**(1/2)
                if diff > 0.1:
                    x = row[0,1]
                    y = row[0,2]
                    z = row[0,3]
                    cord1 = HSF.AddNewPointCoord(x, y, z)
                    hb2.AppendHybridShape(cord1)   
                else:
                    print("point double")
        #update and save file
        part1.Update 
        silo = part.replace('testfiles', 'CAD')    
        partDocument1.SaveAs(silo)
        
        CATIA.RefreshDisplay = True
        print("Time to create splines:--- %s seconds ---" % (time.time() - st42))
        
    
#varVal = {'span': 200,'mesh_size':0.8,'spools':8,'mandrel_speed':1.2,'guide_rad':700,'IMD':100}
#b_master("_test_A008_JK",varVal)