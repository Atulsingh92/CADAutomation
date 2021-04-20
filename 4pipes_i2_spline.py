# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 18:35:59 2021

@author: aus1n19
Changes only diameters of the CAD, with a varying a spline interpolation coefficients.
These coefficients are build using the first entry of the 4 diameter sampling, and then varied randomly to obtain interpolated values for the rest of the 4 diameters for 
n CAD models.
"""

#Common to all
import sys
from matplotlib import pyplot as plt
import numpy as np
import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

#Common to pyKriging
import pyKriging  
from pyKriging.krige import kriging  
from pyKriging.samplingplan import samplingplan
from pyKriging.CrossValidation import Cross_Validation
from pyKriging.utilities import saveModel
#import mayavi.mlab as mlab

#Common to pySW
from pySW import SW
import psutil, time, shutil
from pyDOE import *
from doepy import build

import matplotlib.cm as cm
from scipy import interpolate
import matplotlib.colors as colors
import itertools

import time

k = 13
n = 20

start_time = time.time()
sp = samplingplan(k)  
X = sp.optimallhc(n)



pd.set_option('display.max_columns', None)

partName = r'4pipes_i2.SLDPRT';

if "SLDWORKS.exe" in (p.name() for p in psutil.process_iter()) == False:
    print('starting SLDWORKS')
    SW.startSW();
    time.sleep(10);

SW.connectToSW()

SW.openPrt(psutil.os.getcwd()+'\\'+partName);

var, units, eqnnumber = SW.getGlobalVars(); 

variables = [];
var1 = [];
#diameters=[]
#diameters_index=[]
for i in var:
    var1.append(i); 


diameters_name = [i for i in var1 if 'diameter' in i] #define 
diameters_index=[i for i, j in enumerate(var1) if 'diameter' in j]
#diameters_values = [i for i in var1[range(len(diameters_index[i])]]



def customgauss(mu,sigma):
    while True:
        number = random.gauss(mu,sigma)
        if (number > 0 and number < 1):
            break
    return number

c=[]
for i in range(n):
    c = np.append(c, random.uniform(8,15))

#update diameters with random.gauss
#for i in range(len(diameters_index)):
#   X[:,diameters_index[i]]= import plotly.plotly

driven = []
driven_name = [i for i in var1 if 'td' in i]
driven_index = [i for i, j in enumerate(var1) if 'td' in j]
Xnew = np.delete(X, np.s_[driven_index], axis=1) # delete columns that are driven

var1_delete=[i for i in var1 if 'td' in i]
var1_delete_index = [i for i, j in enumerate(var1) if 'td' in j]
var1new = np.delete(var1, np.s_[var1_delete_index], axis=0)


#that can be set
#in_manifold_l=[100,130]
#in_manifold_w=[50,65]
manifold_length = 100
manifold_width = 40
in_manifold_dia = [15,20]
#z_offset_manifold = [in_manifold_dia[1], manifold_length -in_manifold_dia[1]/2]#20, 90
#y_offset_manifold = [in_manifold_dia[1], manifold_width-in_manifold_dia[1]/2]#20, 30

#tube-1
td1 = [8,15]
#z_1 = [td1[1], in_manifold_l[1]/2 - td1[1]] #[15, 50]
#y_1 = [td1[1], in_manifold_w[0] - td1[1]/2]   #[15, 42.5]

#tube-2
td2 = [8,15]
#z_2= [ in_manifold_l[1]/2 + td2[1] , in_manifold_l[0]-td2[1]] #65,85]
#y_2 = [td2[1], in_manifold_w[0] - td2[1]/2] # 15, 42.5

td3 = [8,15] # mean 11.5, stdev= np.std(x)
#z_3 = [2,5]
#y_3 = [20,67.5]

td4 = [8,15]
#z_4 = [2,5]
#y_4 = [20,67.5]

#side_edge_2_t1 = [10, 25] # [ 7.5+1 , 50] given at random

#top_edge_2_t1 = [10, manifold_width-(td1[1]/2 + 1)]  # 9.5,31.5

#tube_dist = [13,22] # 10, 30


#lhs_in_manifold_l = np.array([], dtype=float)
#lhs_in_manifold_w = np.array([], dtype=float)
lhs_in_manifold_dia = np.array([], dtype=float)
#lhs_horizontal_offset_manifold_d =  np.array([], dtype=float)
#lhs_vertical_offset_manifold_d =  np.array([], dtype=float)
gauss_td1 = np.array([], dtype=float)
gauss_td2 = np.array([], dtype=float)
#lhs_horizontal_td1 = np.array([], dtype=float)
#lhs_vertical_td1 = np.array([], dtype=float)
#lhs_horizontal_td2 = np.array([], dtype=float)
#lhs_vertical_td2 = np.array([], dtype=float)

gauss_td3 = np.array([], dtype=float)
#lhs_horizontal_td3=np.array([], dtype=float)
#lhs_vertical_td3 = np.array([], dtype=float)

gauss_td4=np.array([], dtype=float)
#lhs_horizontal_td4=np.array([], dtype=float)
#lhs_vertical_td4=np.array([], dtype=float)

#lhs_tubedistance = [np.array([], dtype=float)]
#lhs_se2t1 = [np.array([], dtype=float)]
#lhs_te2t1 = [np.array([], dtype=float)]

for i in Xnew[:,0]:
    lhs_in_manifold_dia = np.append(lhs_in_manifold_dia, i*(np.max(in_manifold_dia) - np.min(in_manifold_dia)) + np.min(in_manifold_dia))

#for i in Xnew[:,1]:
 #   lhs_horizontal_offset_manifold_d = np.append(lhs_horizontal_offset_manifold_d, i*(np.max(z_offset_manifold) - np.min(z_offset_manifold)) + np.min(z_offset_manifold))
    
#for i in Xnew[:,2]:
 #   lhs_vertical_offset_manifold_d = np.append(lhs_vertical_offset_manifold_d, i*(np.max(y_offset_manifold) - np.min(y_offset_manifold)) + np.min(y_offset_manifold))

for i in Xnew[:,1]:
    gauss_td1 = np.append(gauss_td1, i*(np.max(td1) - np.min(td1)) + np.min(td1))
    
for i in Xnew[:,2]:
    gauss_td2 = np.append(gauss_td2, i*(np.max(td2) - np.min(td2)) + np.min(td2))
      
for i in Xnew[:,3]:
    gauss_td3 = np.append(gauss_td3,  i*(np.max(td3) - np.min(td3)) + np.min(td3))

for i in Xnew[:,4]:
    gauss_td4 = np.append(gauss_td4, i*(np.max(td4) - np.min(td4)) + np.min(td4))

#for i in Xnew[:,5]:
#    lhs_tubedistance = np.append(lhs_tubedistance, i*(np.max(tube_dist) - np.min(tube_dist)) + np.min(tube_dist))

#for i in Xnew[:,6]:
#    lhs_se2t1 = np.append(lhs_se2t1, i*(np.max(side_edge_2_t1) - np.min(side_edge_2_t1)) + np.min(side_edge_2_t1))

#for i in Xnew[:,7]:
 #   lhs_te2t1 = np.append(lhs_te2t1, i*(np.max(top_edge_2_t1) - np.min(top_edge_2_t1)) + np.min(top_edge_2_t1))
    

mapped_vars=[lhs_in_manifold_dia, gauss_td1, gauss_td2, gauss_td3, gauss_td4]#, lhs_tubedistance, lhs_se2t1, lhs_te2t1]


print("time to generate sampling %s s" % (time.time()-start_time))

np.set_printoptions(threshold=sys.maxsize,precision=2)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
np.set_printoptions(formatter={'str': lambda y: "{0:0.3f}".format(y)})

gauss=[]
for i in range(len(variables)):
    var1new = mapped_vars[i]    


design = np.array(mapped_vars)

d = [list(i) for i in zip(*design)]

des = np.array(d)

s = pd.DataFrame(des, columns = [i for i in var1new])


######################################################################
#Spline generation
x0 = Xnew[0,1:5] # lhs of X for 4 diameters from CAD1
x0.sort()
y0 = des[0,1:5] # diameters for the 4 diameters as baseline
f = interpolate.InterpolatedUnivariateSpline(x0,y0) # spline
##
coeffs_current = []
coeff = f.get_coeffs() #coeffs of spline
y = []
delta = [1,2,3,-1,-2,-3] # delta to change spline with some offsets


for i in range(n):
    change = random.choice(delta) #pick random from delta
    coeffs_current = coeff + change # update coefficients
    for j in range(len(coeffs_current)):
        f.get_coeffs()[j] = coeffs_current[j] #assign to spline
        
    y = np.append(y, f(Xnew[i,1:5])) #calculate with new spline


newd = np.reshape(abs(y), (n , len(Xnew[0,1:5])))


#colormap = plt.cm.gist_ncar

fig, ax = plt.subplots(figsize = (15,7))

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

    
cmap = get_cmap(n)    
for i in range(len(newd)):
    plt.scatter(Xnew[i,1:5], newd[i], label = 'cad'+str(i), color=(random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)))
    plt.pause(0.5)
    plt.savefig('cad'+str(i)+'.png')
    plt.close(fig)

    
plt.show()
plt.legend(bbox_to_anchor=(1.02,1), loc = 'best')

#### Change des to new updated spline values
for i in range(len(des)):
    des[i,1:5] = newd[i]
    
# update s again for cad
s = pd.DataFrame(des, columns = [i for i in var1new])


analysisDir = psutil.os.getcwd()+'\\analysis';
if psutil.os.listdir(psutil.os.getcwd())[0] == 'analysis':
    shutil.rmtree(analysisDir);
    psutil.os.mkdir(analysisDir);
else:
    psutil.os.mkdir(analysisDir); 
for i in range(len(des)): 
    psutil.os.mkdir(analysisDir+'\\'+str(i)); 
    for j in range(len(var1new)): #0to 14
        SW.modifyGlobalVar(var1new[j], des[i][j],'mm');
    
    
    SW.update();    
    SW.save(analysisDir+'\\'+str(i), str(i), 'SLDPRT');

s.to_csv(psutil.os.getcwd()+'\\parameters.csv')

#################################################################
#                       Print CSV's
#################################################################
frames = [s]
masterframe = pd.concat(frames,axis=1)
#print(masterframe)
masterframe.to_csv(psutil.os.getcwd()+'\\Optimal-Physical-sampled.csv')
################################################################

#Prints all design updates!
np.set_printoptions(threshold=sys.maxsize,precision=2)

for i in range(len(des)):
    for j in range(len(var1new)):
        print("at design " + str(i) + " , " + var1new[j] + " is " + str(des[i][j]))
       
#SW.shutSW();  # Closing this causes SW to close, so named selections cannot be carried forward.
               # Do not close SW!




