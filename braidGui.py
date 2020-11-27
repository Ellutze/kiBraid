# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:33:19 2020

@author: jakub.kucera
"""

import PySimpleGUI as sg 
from braid_CATIA import b_master

def bGUI():
    

    
    layout = [[sg.In() ,sg.FileBrowse(file_types=(("Text Files", "*.CATpart"),),key='tf')],[sg.T('no. spools',size=(10, 1)),sg.In(key='spl',size=(5, 1))],
               [sg.T('span',size=(10, 1)),sg.In(key='span',size=(5, 1))],[sg.T('mesh size',size=(10, 1)),sg.In(key='msh',size=(5, 1))],
               [sg.T('mandrel speed',size=(10, 1)),sg.In(key='ms',size=(5, 1))],[sg.T('initial mandrel distance',size=(10, 1)),sg.In(key='IMD',size=(5, 1))],
               [sg.T('guide radius',size=(10, 1)),sg.In(key='gr',size=(5, 1))],
               [sg.Button('RUN')]]    
    window = sg.Window('My window with tabs', layout, default_element_size=(12,1))
    
    #GUI function loop
    while True: 
        #read all potential user inputs
        event, values = window.read()    
        
        if event is None: # always, always give a way out!    
            break  
        if event in 'RUN':
            fll = str(values['tf'])
            print(fll)
            
            fll = fll.replace('''\\''', '''\\\\''')
            print(fll)
            fll = fll.replace("\\\\\\\\","\\\\")
            print(fll)
            
            
            if fll == "":
                print("please select a file")
            else:
                span = float(values['span'])
                msh = float(values['msh'])
                spl = int(values['spl'])
                ms = float(values['ms'])
                gr = float(values['gr'])
                IMD = float(values['IMD'])
                print(fll,span,msh,spl,ms)
            
                varVal = {'span': span,'mesh_size':msh,'spools':spl,'mandrel_speed':ms,'guide_rad':gr,'IMD':IMD}
                b_master(fll,varVal)
                #varVal = {'span': 200,'mesh_size':0.8,'spools':8,'mandrel_speed':1.2,'guide_rad':700,'IMD':100}
                #b_master("_test_A008_JK",varVal)

bGUI()