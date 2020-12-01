# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:33:19 2020

@author: jakub.kucera
"""

import PySimpleGUI as sg 
from braid_CATIA import b_master

def bGUI():
    

    #Layout of the GUI, fields and positions
    layout = [[sg.In(size=(20, 1)) ,sg.FileBrowse(file_types=(("Text Files", "*.CATpart"),),key='tf',size=(7, 1))],
               [sg.T('no. spools',size=(20, 1)),sg.In(key='spl',size=(5, 1))],
               [sg.T('span',size=(20, 1)),sg.In(key='span',size=(5, 1))],
               [sg.T('mesh size',size=(20, 1)),sg.In(key='msh',size=(5, 1))],
               [sg.T('mandrel speed',size=(20, 1)),sg.In(key='ms',size=(5, 1))],
               [sg.T('initial mandrel distance',size=(20, 1)),sg.In(key='IMD',size=(5, 1))],
               [sg.T('guide radius',size=(20, 1)),sg.In(key='gr',size=(5, 1))],
               [sg.Checkbox('CATIA visualisation', default=True,key='vis')],
               [sg.Button('RUN')]]    
    window = sg.Window('My window with tabs', layout, default_element_size=(12,1))
    
    #GUI function loop
    while True: 
        #read all potential user inputs
        event, values = window.read()    
        
        if event is None: # way out 
            break  
        if event in 'RUN':
            fll = str(values['tf'])  
            #turn the input into readable format for CATIA
            fll = fll.encode("unicode_escape").decode()
            fll = fll.replace('/', '\\\\')
            
            if fll == "":
                #in case no file was selected
                print("please select a file")
            else:
                #each of these has to be specified now
                #default values if empty
                if str(values['span']) is not '':
                    span = float(values['span'])
                else:
                    span = 100
                if values['msh'] is not '':
                    msh = float(values['msh'])
                else:
                    msh = 1
                if values['spl'] is not '':    
                    spl = int(values['spl'])
                else:
                    spl = 6
                if values['ms'] is not '':
                    ms = float(values['ms'])
                else:
                    ms = 2
                if values['gr'] is not '':
                    gr = float(values['gr'])
                else:
                    gr = 200
                if values['IMD'] is not '':
                    IMD = float(values['IMD'])
                else:
                    IMD = 500
                    
                #Run the simulation○
                #example input:
                #varVal = {'span': 200,'mesh_size':0.8,'spools':8,'mandrel_speed':1.2,'guide_rad':700,'IMD':100}
                vis = bool(values['vis'])
                varVal = {'span': span,'mesh_size':msh,'spools':spl,'mandrel_speed':ms,'guide_rad':gr,'IMD':IMD}
                b_master(fll,varVal,vis)

bGUI()