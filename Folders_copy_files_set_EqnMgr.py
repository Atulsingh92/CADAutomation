# -*- coding: utf-8 -*-
"""
Created on Thu Apr 8 14:39:06 2021
@author: Atul Singh
"""

#Common to all
import sys
import os
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



k = 2                                                  
n = 7                         # Depends on the availability of computational time
sp = samplingplan(k)  
X = sp.optimallhc(n)

CADfile='pipe.sldprt'
equationsmanager='equations.txt'

length=[100,200,300,400,500]
dia=[9.5,10,10.5,11,11.5]   


lhslen=np.array([], dtype=float)
lhsdia=np.array([], dtype=float)
print(X)

for i in (X[:,0]): 
    lhslen=np.append(lhslen, i*(np.max(length)-np.min(length))+np.min(length))

for i in (X[:,1]):
    lhsdia=np.append(lhsdia, i*(np.max(dia)-np.min(dia))+np.min(dia))

        
print("De-scaled length is:")
print(lhslen)
print("De-scaled dia is:")
print(lhsdia)


##############################################################################
Xdf = pd.DataFrame(X, columns = ['OptimalLength', 'OptimalDiameter']) #, 'OptimalExtrudeL' ,'OptimalDiameter'])
print(Xdf)
##############################################################################

##############################################################################
#                               Dimensions for CAD
##############################################################################
np.set_printoptions(threshold=sys.maxsize,precision=3)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
np.set_printoptions(formatter={'str': lambda y: "{0:0.3f}".format(y)})

print("Dimensions for CAD are:")
print("length at: ")
print(lhslen)
print("diameter")
print(lhsdia)

###sanity check
design = (lhslen, lhsdia)
print(design)
d = [list(i) for i in zip(*design)]
print(d)
des=np.array(d)
print(des)

##############################################################################
# Generating directory to copy CADfile and update equationsmanager for each
##############################################################################
analysisDir = psutil.os.getcwd()+'\\analysis';
if psutil.os.listdir(psutil.os.getcwd())[0] == 'analysis':
    shutil.rmtree(analysisDir);
    psutil.os.mkdir(analysisDir);
else:
    psutil.os.mkdir(analysisDir); #make analysisDir


#copy the cad and equations file.
for i in range(n):
    psutil.os.mkdir(analysisDir+'\\'+str(i)+'directory'); # create number of folders insider analysis directory
    dst = analysisDir+'\\'+str(i)+'directory'
    shutil.copy(psutil.os.getcwd()+'\\'+ CADfile, dst)
    shutil.copy(psutil.os.getcwd()+'\\'+ equationsmanager, dst)
    
  
    
for i in range(n):
    os.chdir(analysisDir+'\\'+str(i)+'directory')
    f=open(equationsmanager,"rt")
    data=f.readlines()
    exl = data[0].split() #add as per variables in EqnMgr ,#exl = ['"extrudelength"=', '100']
    exl[1] = str(np.round(lhslen[i],3)) # exl = ['"extrudelength"=', '414.286']
    update_exl = ''.join(exl)    # '"extrudelength"=414.286'
    data[0] = str(update_exl)+'\n'
    td = data[2].split()
    td[1]=str(np.round(lhsdia[i],2))
    update_td = ''.join(td)
    data[2] = str(update_td)+'\n'
    f.close()
    with open(equationsmanager, 'w') as f:
        for line in data:
            f.write(line)
    f.close()  
