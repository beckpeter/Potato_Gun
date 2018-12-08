# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:56:58 2018

@author: beckp
"""
# imports
import numpy as np
import pandas as pd
import cantera as ct
import matplotlib.pyplot as plt
'''
Variables
'''
#pipe dimensions
d1 = 3 * 0.0254  #3 in
L1 = 36 * 0.0254 #3 ft

d2 = 0.375 * 0.0254 # 3/8 in (total guess at hydraulic diameter)
L2 = 4 * 0.0254 #4 in

d3 = 1.5 * 0.0254 #1.5 in
L3 = 24 * 0.0254  #2 ft

#Pressure
P_atm = 101325
P_0 = 110 * 6894.76 + P_atm #pressure that we fill chamber up to = 110 psi + 1atm (absolute)

#Temp
T = 293.15  #Kelvin

#step size
dr = 0.001 # 1mm
dtheta = 45 # degrees
dz = dr  # 1mm_ initial dz
dt = 0.001 #s
t_max = 10 #s

'''
Start Of Code
'''

## calculations 
A1 = np.pi/4 * d1**2
A2 = np.pi/4 * d2**2
A3 = np.pi/4 * d3**2
## Gas def
air_atm = ct.Solution('air.xml')

'''
1-d Analysis
'''
#create table to save data in
fluid_elements = {'zloc':np.arange(dz/2,L1+L2,dz),'dz':dz}
fluid_elements = pd.DataFrame(fluid_elements)
fluid_elements['area'] = [A1 if z <= L1 else A2 if z<=L1+L2 else A3 for z in fluid_elements.zloc]
fluid_elements['press'] = [P_0 if z <= L1 else P_atm for z in fluid_elements.zloc]
#fluid_elements.state = [ct.Solution('air.xml') for i in fluid_elements.index]

#plot of initial pressure
fluid_elements.plot(x='zloc',y='press')


#1-d sim










#plot of final press
#fluid_elements.plot(x='zloc',y='press')












