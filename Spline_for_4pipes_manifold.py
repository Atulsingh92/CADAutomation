# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:36:37 2021

@author: aus1n19
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import BSpline
n =20
des = [[16.62, 11.32,  9.22, 12.38,  8.53],
       [18.38, 14.48, 12.38, 14.82, 10.97],
       [17.88,  8.53, 14.82,  9.57,  9.93],
       [15.62, 14.12, 14.12, 13.07,  9.57],
       [15.88, 11.68, 13.43,  9.93, 13.77],
       [17.62, 13.07, 10.28, 13.77, 12.38],
       [18.62,  9.22, 10.62, 14.12, 11.32],
       [17.38, 12.73, 14.48,  8.88, 13.43],
       [19.38, 10.28, 12.02, 10.28, 14.48],
       [15.12,  8.88, 12.73,  8.53, 12.02],
       [19.88, 12.38,  9.93, 10.97,  9.22],
       [16.38,  8.18, 13.07, 14.48, 12.73],
       [16.12, 13.43, 11.68, 13.43,  8.18],
       [19.12, 10.97, 13.77, 11.68, 10.28],
       [15.38, 12.02, 11.32, 12.02,  8.88],
       [19.62,  9.57,  9.57, 10.62, 11.68],
       [18.12,  9.93,  8.18, 12.73, 14.82],
       [17.12, 10.62,  8.53,  9.22, 13.07],
       [16.88, 14.82,  8.88, 11.32, 14.12],
       [18.88, 13.77, 10.97,  8.18, 10.62]]

des = np.array(des)


x_for_function = np.linspace(0,1,20)
              
xp = np.linspace(0,1,4)
yp = des[:,1:5][0]  #change this one by one

eval_here = [0.1,  0.4, 0.8, 0.95]

#t_interp = np.interp(eval_here, xp, yp)
#t_int1d = interpolate.interp1d(xp,yp, kind='cubic') # does not have coefficients call 
#yint1d = t_int1d(eval_here)
y_spline  =[]
y_all = []
fig,ax =plt.subplots(figsize=(12,8))

for i in range(n):
    yp = des[:,1:5][i]
    t_int1d = interpolate.interp1d(xp,yp, kind='cubic') #can be cubic
    yint1d = t_int1d(eval_here)
    x_spline = np.linspace(0,1,200)
    a_spline = interpolate.make_interp_spline(eval_here, yint1d, k=3) # has coefficients
    y_spline = a_spline(x_spline)
    y_all = np.append(y_all, y_spline)
    plt.plot(x_spline, y_spline, '-', label ='Curve for CAD '+str(i) )
    plt.scatter(eval_here, yint1d)#, label='CAD '+str(i))


#y_all_reshape = np.reshape(y_all, (n, )
#plt.scatter(xp,yp,label= 'fx')
#plt.plot(eval_here, t_interp, 'o', label = 'np.interp')
#plt.plot(eval_here, yint1d, '-x', label  = 'scipy.int1d')
plt.margins(x=0)
plt.legend(bbox_to_anchor=(1.02,1))
plt.tight_layout()
