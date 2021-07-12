# -*- coding: utf-8 -*-
"""
Maximize: f1 = 0.047 * pow( x[:,0], 0.8121) * pow(x[:,1],0.1233) * pow(x[:,2], -0.1585)
Minimize f2 = f2 = 9.795 * pow( x[:,0], 0.8014) * pow(x[:,1],0.8437) * pow(x[:,2], -0.6462)

Subject to 
1) 10020 <= Reynolds <= 40060
2) 0.02 <= height <= 0.08
3) 1.0 <= pitch <= 2.0

"""


import numpy as np
import math as m
import matplotlib.pyplot as plt

import autograd.numpy as anp
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.util.misc import stack
from pymoo.visualization.scatter import Scatter
from pymoo.factory import get_visualization

from pymoo.performance_indicator.hv import Hypervolume

from pymoo.factory import get_problem, get_reference_directions
from pymoo.visualization.pcp import PCP
from pymoo.util.display import MultiObjectiveDisplay
from pyrecorder.video import Video
from pyrecorder.recorders.file import File

#ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=2)

class MyProb(Problem):
    
    def __init__(self):
        super().__init__(n_var = 3,
                         n_obj = 2,
                         n_constr = 0,
                         ################   0=Re, 1=e/D , 2=p/D ################
                         xl = anp.array([10000, 0.06, 0.8]),
                         xu = anp.array([35000, 0.12, 1.5]))
                         
    
    def _evaluate(self, x, out, *args, **kwargs):
        #Nu = [209.46053, 160.35194, 183.18598, 225.42131, 122.72628, 210.99603, 267.90623, 231.49742, 126.67416, 184.65538]
        #ff1 = [0.10041, 0.05382, 0.06818, 0.05726, 0.14122, 0.07696, 0.07909, 0.03519, 0.0744 ,0.08876]
        #ff = [-1*x for x in ff1]
        #f1 = 94.3768 * pow(x[:,0], 0.0000344) * pow(x[:,2], 0.8121) * pow(x[:,1], -0.5745) 
        #f2 = 0.1341 * pow(x[:0], -0.000011) * pow(x[:,2], -0.5745) * pow(x[:,1], 3.4097)*-1
        #f1 = 0.047 * pow( x[:,0], 0.8121) * pow(x[:,1],0.1233) * pow(x[:,2], -0.1585)
        #f2 = 9.795 * pow( x[:,0], 0.8014) * pow(x[:,1],0.8437) * pow(x[:,2], -0.6462) * -1
        Nu1= m.exp(6.1949) * pow(x[:,0], -0.2858) * pow(x[:,2], -0.0356) * pow(x[:,1], -0.0819)
        ff = m.exp(2.3258) * pow(x[:,0], -0.3119) * pow(x[:,2], -1.0354) * pow(x[:,1], 0.7006)
        Nu = [-1*x for x in Nu1]
        out["F"] = anp.column_stack([Nu,ff])
        #out["G"] = anp.column_stack([0,0])    




class MyDisplay(MultiObjectiveDisplay):
    def _do(self,problem, evaluator, algorithm):
        super()._do(problem,evaluator,algorithm)
        X = algorithm.opt.X
        self.output.append("x0", X[0])
        self.output.append("x1", X[1])
        self.output.append("x2", X[2])
        
        
        
problem=MyProb()

algorithm = NSGA2(
        pop_size = 100,
        n_offsprings = 10,
        sampling = get_sampling("real_random"),
        crossover = get_crossover("real_sbx", prob = 0.9, eta = 15),
        mutation = get_mutation("real_pm", eta=20),
        eliminate_duplicates = True
        )


res = minimize(MyProb(), 
               algorithm, 
               ("n_gen", 500), 
               seed =1, 
               pf = problem.pareto_front(use_cache=False),
               save_history=True,
               verbose= True)


Scatter().add(res.F).show()

dspace = res.pop.get("X")
reynolds = dspace[:,0]
pitch= dspace[:,1]
depth = dspace[:,2]
#print(dspace)


metric = Hypervolume(ref_point=np.array([1.0, 1.0]))

# collect the population in each generation
pop_each_gen = [a.pop for a in res.history]

# receive the population in each generation
obj_and_feasible_each_gen = [pop[pop.get("feasible")[:,0]].get("F") for pop in pop_each_gen]

# calculate for each generation the HV metric
hv = [metric.calc(f) for f in obj_and_feasible_each_gen]

# visualze the convergence curve
plt.plot(np.arange(len(hv)), hv, '-o')
plt.title("Convergence")
plt.xlabel("Generation")
plt.ylabel("Hypervolume")
plt.show()


ps = problem.pareto_set(use_cache=False, flatten=False)
pf = problem.pareto_front(use_cache=False, flatten=False)

# Design Space
#plot = Scatter(title = "Design Space", axis_labels="x")
#plot.add(res.X, s=30, facecolors='none', edgecolors='r') #res.X design space values
#plot.add(ps, plot_type="line", color="black", alpha=0.7)
#plot.do()
#plot.do()
#plot.apply(lambda ax: ax.set_xlim(0, 300))
#plot.apply(lambda ax: ax.set_ylim(10000, 35000))
#plot.show()

# Objective Space
plot = Scatter(title = "Objective Space", legend=True)
plot.add(res.F, label="ND Solutions") # res.F are objective space vlaues
plot.add(res.history[0].pop.get("F"), label="DOE")
plot.add(pf, plot_type="line", color="black", alpha=0.7)
plot.show()


#video 


        
        
    
with Video(File("scratch.mp4")) as vid:
    for entry in res.history:
        if entry.n_gen%5:
            fig,(ax1,ax2) = plt.subplots(2, figsize=(8,4))
            PCP(ax=ax1).add(entry.pop.get("X")).do()
            Scatter(ax=ax2).add(entry.pop.get("F")).do()
            vid.record(fig=fig)
            
            
 # Parallel chart plot
plot3 = PCP(title=("Obejctive functions", {'pad': 30}),
           n_ticks=5,
           #legend=(True, {'loc': "upper left"}),
           labels=["Reynolds number", "e/D", "p/D"]).add(entry.pop.get("X")).do()
plot3.set_axis_style(color="grey", alpha=1)
plot3.add(dspace, color="grey", alpha=0.3)
plot3.show()
