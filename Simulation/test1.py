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
P_0 = 110 * 6894.76 + P_atm #pressure that we fill chamber up to

#Temp
T = 293.15  #Kelvin

#step size
dr = 0.001 # 1mm
dtheta = 45 # degrees
dz = dr  # 1mm
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
z_points = np.arange(0,L1+L2+L3,dz)

## to do: make these using list comprehension
## to do: turn these all into another datatype.  Maybe a pandas array
P_list = []
for point in z_points:
    if point <=L1:
        P_list.append(P_0)
    else:
        P_list.append(P_atm)
        
air = ct.Solution('air.xml')
cantera_list = []
for point in range(len(z_points)):
    if z_points[point] <=L1:
        air.TP = T,P_0
    else:
        air.TP = T,P_0
    cantera_list.append(air)

v_list = []
for point in range(len(z_points)):
    v_list.append(0)
    
A_list = []
for point in range(len(z_points)):
    if z_points[point] <= L1:
        A_list.append(A1)
    elif z_points[point] <= L1+L2:
        A_list.append(A2)
    else:
        A_list.append(A3)
t_list = np.arange(0,t_max,dt)


##
  
plt.plot(z_points,P_list)
plt.show()
##actual sim
 
massflux_list = []
for point in range(len(z_points)):
    massflux_list.append(0)  
#mass_list = []
#for point in range(len(z_points)):
#    mass_list.append(cantera_list[point].density * A_list[point] * dz)  
for point in range(len(z_points)-1):
    ##acceleration of fluid body due to pressure difference
    dP = cantera_list[point].P - cantera_list[point+1].P
    
#    momentum change is due to impulse -> d(mv) = F* dt
    mv = dP * A_list[point] *dt
#    v_new = v_old + momentum change / mass
    v_list[point] = v_list[point] + mv / (cantera_list[point].density * A_list[point] * dz)

    #to do: account for different areas
    #isentropic expansion (aka polytropic with n = k)
    #new_cantera = f(old_entropy, new specific volume)
    cantera_list[point].SV = cantera_list[point].s, ((dz+v_list[point]*dt)*A_list[point]/(cantera_list[point].density * A_list[point] * dz))
    
    #mass flux due to velocity
    try:
        vdt = v_list[point] * dt
        if vdt>0:
            print(vdt)
        if np.ceil(vdt)>0:
            for i in range(np.floor(vdt)):
                massflux_list[point+i] += cantera_list[point].density* A_list[point]* dz
            massflux_list[point + np.ceil(vdt)] = (vdt - np.floor(vdt)) * cantera_list[point].density* A_list[point]* dz
        elif np.ceil(vdt)<0:
            vdt = -vdt
            for i in range(np.floor(vdt)):
                massflux_list[point-i] += cantera_list[point].density* A_list[point]* dz
            massflux_list[point - np.ceil(vdt)] = (vdt - np.floor(vdt)) * cantera_list[point].density* A_list[point]* dz
    except:
        pass
for point in range(len(z_points)-1):
    cantera_list[point].SV = cantera_list[point].s, (dz*A_list[point]/(cantera_list[point].density * A_list[point] * dz + massflux_list[point]))
    P_list[point] = cantera_list[point].P

  
plt.plot(z_points,P_list)
plt.show()






