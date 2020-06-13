# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:37:02 2020
@author: Atul Singh
Purpose is to combine PyKriging 's sampling capabilities, to pySW's generative
capabilities.
So, an LHC sampled in pyKriging will generate dimensions to be feed to a 
parameterised CAD in Solidworks.
This generates the "Optimal LHC" cad models.
--> Requires PySW
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
import mayavi.mlab as mlab

#Common to pySW
from pySW import SW
import psutil, time, shutil
from pyDOE import *
from doepy import build



k = 4                            # Reynolds, Pitch/depth, groove/depth, diameter.
                                 # Changing this, requires changes in arrays for pySW    
n = 7                            # Depends on the availability of computational time
sp = samplingplan(k)  
X = sp.optimallhc(n)

Rey=[10000,15000,20000,25000,30000,35000] # Decide what reynolds range to be looked at!
pbyD=np.arange(1,3,0.5)                   # Decide the range of pitch to depth ratios !
ebyD=np.arange(0.1,0.2,0.025)             # Decide range of groove depth ratios!

D=[6,8,10,12,15]                          # Decide the range of Dimensions

lhsre=np.array([], dtype=float)
lhse=np.array([], dtype=float)
lhsp=np.array([], dtype=float)
lhsD=np.array([], dtype=float)

for i in (X[:,0]): #Assigned Reynolds
    lhsre=np.append(lhsre, i*(np.max(Rey)-np.min(Rey))+np.min(Rey))

for i in (X[:,1]): #Assigned e/d
    lhse=np.append(lhse, i*(np.max(ebyD)-np.min(ebyD))+np.min(ebyD))

for i in (X[:,2]): #Assigned p/d
    lhsp=np.append(lhsp, i*(np.max(pbyD)-np.min(pbyD))+np.min(pbyD))

for i in (X[:,3]): #Assigned D
    lhsD=np.append(lhsD, i*(np.max(D)-np.min(D))+np.min(D))
        
print("De-scaled Reynolds is:")
print(lhsre)
print("De-scaled pitch/dia is:")
print(lhsp)
print("De-scaled groovedepth/dia is:")
print(lhse)
print("De-scaled Diameters are :")
print(lhsD)


##############################################################################
Xdf = pd.DataFrame(X, columns = ['OptimalReynolds', 'OptimalGrooveD', 'OptimalExtrudeL' ,'OptimalDiameter'])
print(Xdf)
##############################################################################

##############################################################################
#                               Dimensions for CAD
##############################################################################
np.set_printoptions(threshold=sys.maxsize,precision=2)

p = lhsp*lhsD
e = lhse*lhsD
print("Dimensions for CAD are:")
print("Reynolds at: ")
print(lhsre)
print("Pitch, (=Extrude Length)")
print(p)
print("Groove depth")
print(e*2)
print(e)
print("Diamters: ")
print(lhsD)

##############################################################################
#                               Generating CAD
##############################################################################

pd.set_option('display.max_columns', None)

partName = r'CorrugatedTube-Parameterized.SLDPRT'; #Should have global variable
                                                   # and equations already defined.

if "SLDWORKS.exe" in (p.name() for p in psutil.process_iter()) == False:
    print('starting SLDWORKS')
    SW.startSW();
    time.sleep(10);

SW.connectToSW()

SW.openPrt(psutil.os.getcwd()+'\\'+partName);

var = SW.getGlobalVariables(); #example var = {'Dia': 12, 'ExL':12, 'blends':0.5}

variables = [];
var1 = [];
for key in var:
    var1.append(key); #variables_1 = ['Dia', 'ExL' , 'etc' , 'blends']

print("All variables present are: \n" )
print(var)
#  Outputs { 'Diameter': 0,      #0
#            'ExtrudeLength': 2, #1
#            'helixbase': 4,     #2
#            'pitch_ht': 6,      #3
#            'pitch': 8,         #4
#            'grooveD': 9,       #5
#            'blends': 11}       #6
# # Because this is the order defined in solidworks for this CAD

print(var1)
variables = [var1[0],var1[1],var1[5]]   #increase or decrease as k changes
print("CAD variables are : ")
print(variables)

design=[]

var1[0] = lhsD
var1[1] = p
var1[5] = e*2

design=(var1[0],var1[1],var1[5])  #is Tuple

d=[list(i) for i in zip(*design)] #is List

des = np.array(d) 
# s gives the list of updated CAD parameters, minus the Reynolds, as Reynolds
# is not a CAD variable.
s = pd.DataFrame(des, columns = [variables[0],variables[1],variables[2]]) #change as per added variables

analysisDir = psutil.os.getcwd()+'\\analysis';
if psutil.os.listdir(psutil.os.getcwd())[0] == 'analysis':
    shutil.rmtree(analysisDir);
    psutil.os.mkdir(analysisDir);
else:
    psutil.os.mkdir(analysisDir); # make analysis directory folder
for i in range(len(des)): 
    psutil.os.mkdir(analysisDir+'\\'+str(i)); # create number of folders insider analysis directory
    for j in range(len(variables)):
        SW.modifyGlobalVar(variables[j], des[i][j],'mm');
        SW.updatePrt();
        
    SW.saveAssy(analysisDir+'\\'+str(i), str(i), 'SLDPRT');

s.to_csv(psutil.os.getcwd()+'\\parameters.csv')

print("The numpy array to change SW is: ")
print(s)

#print(type(des), type(variables), type(s), type(s_1))
print("The design that will update are " )
print(des)

################################################################################
#                       Print CSV's
################################################################################
frames = [Xdf, s]
masterframe = pd.concat(frames,axis=1)
print(masterframe)
masterframe.to_csv(psutil.os.getcwd()+'\\Optimal-Physical-sampled.csv')
##############################################################################

#Prints all design updates!
np.set_printoptions(threshold=sys.maxsize,precision=2)

for i in range(len(des)):
    for j in range(len(variables)):
        print("at design " + str(i) + "," + variables[j] + " will update to " + str(des[i][j]))

#SW.shutSW();  # Closing this causes SW to close, so named selections cannot be carried forward.
               # Do not close SW!

################################################################################

