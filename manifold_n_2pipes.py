"""
For pipe and plates HX model, without fins!
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

import time

k = 11                                                           
n = 10                         

start_time = time.time()
sp = samplingplan(k)  
X = sp.optimallhc(n)

pd.set_option('display.max_columns', None)

partName = r'manifold_n_2pipes.sldprt';

if "SLDWORKS.exe" in (p.name() for p in psutil.process_iter()) == False:
    print('starting SLDWORKS')
    SW.startSW();
    time.sleep(10);

SW.connectToSW()

SW.openPrt(psutil.os.getcwd()+'\\'+partName);

var = SW.getGlobalVars(); 
print("\nresult of SW.getGlobalVars() is \n" )
print(var) #is tuple
print("\n")

variables = [];
var1 = [];
for key in var[0]:
    var1.append(key); #var1 = ['length', 'tubedia' ] #islist

print(var1)
#that can be set
in_manifold_l=[100,200]
in_manifold_w=[50,100]
in_manifold_dia = [10,20]
z_offset_manifold = [in_manifold_dia[0]/2, in_manifold_l[1]-in_manifold_dia[0]/2]
y_offset_manifold = [in_manifold_dia[0]/2, in_manifold_w[1]-in_manifold_dia[0]/2]
td1 = [8,15]
td2 = [8,15]
z_td1 = [td1[0]/2, in_manifold_l[1]/2 - td1[0]/2] #=[4,46] handles 0 to 50 of min l
y_td1 = [td1[0]/2, in_manifold_w[1]/2 - td1[0]/2]
 # = [4,21] = 
z_td2= [ in_manifold_l[0]/2 + td2[0]/2, in_manifold_l[0] - td2[0]/2] # handles 50 to 100 of minl
# = [54,96]
y_td2 = [td2[0]/2, in_manifold_w[1]/2 + td2[0]/2]

lhs_in_manifold_l = np.array([], dtype=float)
lhs_in_manifold_w = np.array([], dtype=float)
lhs_in_manifold_dia = np.array([], dtype=float)
lhs_horizontal_offset_manifold_d =  np.array([], dtype=float)
lhs_vertical_offset_manifold_d =  np.array([], dtype=float)
lhs_td1 = np.array([], dtype=float)
lhs_td2 = np.array([], dtype=float)
lhs_horizontal_td1 = np.array([], dtype=float)
lhs_vertical_td1 = np.array([], dtype=float)
lhs_horizontal_td2 = np.array([], dtype=float)
lhs_vertical_td2 = np.array([], dtype=float)


for i in X[:,0]:
    lhs_in_manifold_l = np.append(lhs_in_manifold_l, i*(np.max(in_manifold_l)-np.min(in_manifold_l))+np.min(in_manifold_l))

for i in X[:,1]:
    lhs_in_manifold_w = np.append(lhs_in_manifold_w, i*(np.max(in_manifold_w)-np.min(in_manifold_w))+np.min(in_manifold_w))

for i in X[:,2]:
    lhs_in_manifold_dia = np.append(lhs_in_manifold_dia, i*(np.max(in_manifold_dia) - np.min(in_manifold_dia)) + np.min(in_manifold_dia))

for i in X[:,3]:
    lhs_horizontal_offset_manifold_d = np.append(lhs_horizontal_offset_manifold_d, i*(np.max(z_offset_manifold) - np.min(z_offset_manifold)) + np.min(z_offset_manifold))
    
for i in X[:,4]:
    lhs_vertical_offset_manifold_d = np.append(lhs_vertical_offset_manifold_d, i*(np.max(y_offset_manifold) - np.min(y_offset_manifold)) + np.min(y_offset_manifold))

for i in X[:,5]:
    lhs_td1 = np.append(lhs_td1, i*(np.max(td1) - np.min(td1)) + np.min(td1))
    
for i in X[:,6]:
    lhs_td2 = np.append(lhs_td2, i*(np.max(td2) - np.min(td2)) + np.min(td2))
    
for i in X[:,7]:
    lhs_horizontal_td1 = np.append(lhs_horizontal_td1, i*(np.max(z_td1) - np.min(z_td1)) + np.min(z_td1))
    
for i in X[:,8]:
    lhs_vertical_td1 = np.append(lhs_vertical_td1, i*(np.max(y_td1) - np.min(y_td1)) + np.min(y_td1))

for i in X[:,9]:
    lhs_horizontal_td2 = np.append(lhs_horizontal_td2, i*(np.max(z_td2) - np.min(z_td2)) + np.min(z_td2))
    
for i in X[:,10]:
    lhs_vertical_td2 = np.append(lhs_vertical_td2, i*(np.max(y_td2) - np.min(y_td2)) + np.min(y_td2))

lhs_vars=[lhs_in_manifold_l, lhs_in_manifold_w, lhs_in_manifold_dia, lhs_horizontal_offset_manifold_d, lhs_vertical_offset_manifold_d, lhs_td1, lhs_horizontal_td1, lhs_vertical_td1, lhs_horizontal_td2, lhs_vertical_td2, lhs_td2]


print("Des space")
print(X)
print("in_manifold_l for CAD")
print(lhs_in_manifold_l)

print("in_manifold_w for CAD")
print(lhs_in_manifold_w)

print("in_manifold_dia for CAD")
print(lhs_in_manifold_dia)

print("z_offset_manifold_d")
print(lhs_horizontal_offset_manifold_d)

print("y_offset_manifold_d")
print(lhs_vertical_offset_manifold_d)

print("tube_d_1")
print(lhs_td1)

print("lhs_td_2")
print(lhs_td2)

print("horizontal_td1")
print(lhs_horizontal_td1)

print("vertical_td1")
print(lhs_vertical_td1)

print("lhs_horizontal_td2")
print(lhs_horizontal_td2)

print("lhs_vertical_td2")
print(lhs_vertical_td2)


print("time to generate sampling %s s" % (time.time()-start_time))


for i in range(len(variables)):
    var1 = lhs_vars[i]

print(variables)
print(var1)
print(lhs_vars)
des = np.array(lhs_vars)


d = [list(i) for i in zip(*des)]
print(d)

d1 = np.array(d)
print(d1)
s = pd.DataFrame(d1, columns = [i for i in var1])
print(s)


#########################################################################

analysisDir = psutil.os.getcwd()+'\\analysis';
if psutil.os.listdir(psutil.os.getcwd())[0] == 'analysis':
    shutil.rmtree(analysisDir);
    psutil.os.mkdir(analysisDir);
else:
    psutil.os.mkdir(analysisDir); # make analysis directory folder
for i in range(len(des)): 
    psutil.os.mkdir(analysisDir+'\\'+str(i)); # create number of folders
    for j in range(len(variables)):
        SW.modifyGlobalVar(variables[j], des[i][j],'mm');
        SW.update();
        
    SW.save(analysisDir+'\\'+str(i), str(i), 'SLDPRT');

s.to_csv(psutil.os.getcwd()+'\\parameters.csv')

print("The numpy array to change SW is: ")
print(s)

#print(type(des), type(variables), type(s), type(s_1))
print("The design that will update are " )
print(des)

################################################################################
#                       Print CSV's
################################################################################
frames = [s]
masterframe = pd.concat(frames,axis=1)
print(masterframe)
masterframe.to_csv(psutil.os.getcwd()+'\\Optimal-Physical-sampled.csv')
##############################################################################
"""
#Prints all design updates!
np.set_printoptions(threshold=sys.maxsize,precision=2)

for i in range(len(des)):
    for j in range(len(var1)):
        print("at design " + str(i) + "," + var1[j] + " will update to " + str(des[i][j]))

#SW.shutSW();  # Closing this causes SW to close, so named selections cannot be carried forward.
               # Do not close SW!

################################################################################
"""
"""
sp = samplingplan(k)  
X = sp.optimallhc(n)

#set variable range
#those from CAD
in_manifold_length=[100,200]
in_manifold_width=[50,100]
inlet_manifold_dia = [10,20]

#those to be calculated after sampling is set

horizontal_d_inmanifold= range (dia/2, length - d/2)
vertical_d_inmanifold = range( dia/2, width - d/2)

    
max_edge_length_vertical=[]
for i in inlet_manifold_dia:
    min_edge_length_horizontal = np.append(min_edge_length_horizontal, i/2)


for j in in_manifold_length:
        max_edge_length_vertical = np.append(max_edge_length_vertical, j - [i/2 for i in inlet_manifold_dia])
       

##############################################################################
Xdf = pd.DataFrame(X, columns = ['OptimalLength', 'OptimalDiameter'])
print(Xdf)
##############################################################################

##############################################################################
#                               Dimensions for CAD
##############################################################################
np.set_printoptions(threshold=sys.maxsize,precision=2)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
np.set_printoptions(formatter={'str': lambda y: "{0:0.3f}".format(y)})


#get edge limits and define constraints for manifold_inlet 
min_l = np.array([], dtype=float)
max_l = np.array([], dtype=float)
for i,j in zip(lhs_in_manifold_dia, lhs_in_manifold_l):
    min_l = np.append(min_l,j/2)
    max_l = np.append(max_l, j - i/2)


range_inmanifold_circle = np.array([], dtype=float)
for i, j in zip(min_l, max_l):
    range_inmanifold_circle = np.append(range_inmanifold_circle, [i,j])
    
lhs_x = np.array([], dtype=float)
lhs_y = np.array([], dtype=float)
"""