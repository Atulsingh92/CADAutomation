# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:19:56 2023

@author: aus1n19

Maximize: f1 = 0.047 * pow( x[:,0], 0.8121) * pow(x[:,1],0.1233) * pow(x[:,2], -0.1585)
Minimize f2 = f2 = 9.795 * pow( x[:,0], 0.8014) * pow(x[:,1],0.8437) * pow(x[:,2], -0.6462)

Subject to 
1) 10020 <= Reynolds <= 40060
2) 0.02 <= height <= 0.08
3) 1.0 <= pitch <= 2.0


for pymoo version 0.5.0
"""


import numpy as np
import math as m
import matplotlib.pyplot as plt

import autograd.numpy as anp
# from pymoo.core.problem import Problem
# from pymoo.algorithms.moo import nsga2 as NSGA2
# from pymoo.core.sampling import Sampling as sampling
# from pymoo.model.problem import Problem
# from pymoo import *
# from pymoo.model.problem import Problem

# from pymoo.algorithms.nsga2 import NSGA2
# from pymoo.factory import get_sampling, get_crossover, get_mutation
# from pymoo.optimize import minimize
# from pymoo.util.misc import stack
from pymoo.visualization.scatter import Scatter
# from pymoo.factory import get_visualization

# from pymoo.performance_indicator.hv import Hypervolume

# from pymoo.factory import get_problem, get_reference_directions, get_decomposition
from pymoo.visualization.pcp import PCP
# from pymoo.util.display import MultiObjectiveDisplay
# from pyrecorder.video import Video
# from pyrecorder.recorders.file import File


from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_decomposition
from pymoo.optimize import minimize
from pymoo.indicators.hv import Hypervolume

class MyProb(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=3,
                         n_obj=2,
                         #n_constr=2,
                         xl = np.array([10000, 0.06, 0.8]),
                         xu = np.array([35000, 0.12, 1.5]))

    def _evaluate(self, x, out, *args, **kwargs):
        #Nu = [209.46053, 160.35194, 183.18598, 225.42131, 122.72628, 210.99603, 267.90623, 231.49742, 126.67416, 184.65538]
        #ff1 = [0.10041, 0.05382, 0.06818, 0.05726, 0.14122, 0.07696, 0.07909, 0.03519, 0.0744 ,0.08876]
        #ff = [-1*x for x in ff1]
        #f1 = 94.3768 * pow(x[:,0], 0.0000344) * pow(x[:,2], 0.8121) * pow(x[:,1], -0.5745) 
        #f2 = 0.1341 * pow(x[:0], -0.000011) * pow(x[:,2], -0.5745) * pow(x[:,1], 3.4097)*-1
        #f1 = 0.047 * pow( x[:,0], 0.8121) * pow(x[:,1],0.1233) * pow(x[:,2], -0.1585)
        #f2 = 9.795 * pow( x[:,0], 0.8014) * pow(x[:,1],0.8437) * pow(x[:,2], -0.6462) * -1
        Nu1= m.exp(6.1949) * pow(x[0], -0.2858) * pow(x[2], -0.0356) * pow(x[1], -0.0819)
        ff = m.exp(2.3258) * pow(x[0], -0.3119) * pow(x[2], -1.0354) * pow(x[1], 0.7006)
        # Nu = [-1*x for x in Nu1]
        out["F"] = anp.column_stack([-Nu1,ff])


problem = MyProb()

#ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=2)

# class MyDisplay(MultiObjectiveDisplay):
#     def _do(self,problem, evaluator, algorithm):
#         super()._do(problem,evaluator,algorithm)
#         X = algorithm.opt.X
#         self.output.append("x0", X[0])
#         self.output.append("x1", X[1])
#         self.output.append("x2", X[2])

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
               ("n_gen", 300), 
               seed =1, 
               pf = problem.pareto_front(use_cache=False),
               save_history=True,
               verbose= True)


#Scatter plot
Scatter().add(res.F).show()
dspace = res.pop.get("X")
reynolds = dspace[:,0]
pitch= dspace[:,1]
depth = dspace[:,2]
#print(dspace)

n_evals = []             # corresponding number of function evaluations\
hist_F = []              # the objective space values in each generation
hist_cv = []             # constraint violation in each generation
hist_cv_avg = []         # average constraint violation in the whole population

hist = res.history
X, F = res.opt.get("X", "F")

for algo in hist:

    # store the number of function evaluations
    n_evals.append(algo.evaluator.n_eval)

    # retrieve the optimum from the algorithm
    opt = algo.opt

    # store the least contraint violation and the average in each population
    hist_cv.append(opt.get("CV").min())
    hist_cv_avg.append(algo.pop.get("CV").mean())

    # filter out only the feasible and append and objective space values
    feas = np.where(opt.get("feasible"))[0]
    hist_F.append(opt.get("F")[feas])

approx_ideal = F.min(axis=0)
approx_nadir = F.max(axis=0)
metric = Hypervolume(ref_point= np.array([1.1, 1.1]),
                     norm_ref_point=False,
                     zero_to_one=True,
                     ideal=approx_ideal,
                     nadir=approx_nadir)

hv = [metric.do(_F) for _F in hist_F]

plt.figure(figsize=(7, 5))
plt.plot(n_evals, hv,  color='black', lw=0.7, label="Avg. CV of Pop")
plt.scatter(n_evals, hv,  facecolor="none", edgecolor='black', marker="p")
plt.title("Convergence")
plt.xlabel("Function Evaluations")
plt.ylabel("Hypervolume")
plt.show()


# metric = Hypervolume(ref_point=np.array([1.0, 1.0]))

# # collect the population in each generation
# pop_each_gen = [a.pop for a in res.history]

# # receive the population in each generation
# obj_and_feasible_each_gen = [pop[pop.get("feasible")[:,0]].get("F") for pop in pop_each_gen]

# # calculate for each generation the HV metric
# hv = [metric.calc(f) for f in obj_and_feasible_each_gen]

# # visualze the convergence curve
# plt.plot(np.arange(len(hv)), hv, '-o')
# plt.title("Convergence")
# plt.xlabel("Generation")
# plt.ylabel("Hypervolume")
# plt.show()

ps = problem.pareto_set(use_cache=False, flatten=False)
pf = problem.pareto_front(use_cache=False, flatten=False)

# Design Space
plot = Scatter(title = "Design Space", axis_labels="x")
plot.add(res.X, s=30, facecolors='none', edgecolors='r') #res.X design space values
plot.add(ps, plot_type="line", color="black", alpha=0.7)
plot.do()
plot.do()
plot.apply(lambda ax: ax.set_xlim(0, 300))
plot.apply(lambda ax: ax.set_ylim(10000, 35000))
plot.show()




#video 
# The below should be edited with and without .add(entry.pop.get("X").do())
"""
with Video(File("scratch.mp4")) as vid:
    for entry in res.history:
        if entry.n_gen%5:
            fig,(ax1,ax2) = plt.subplots(2, figsize=(8,4))
            PCP(ax=ax1,n_ticks=5,
            #legend=(True, {'loc': "upper left"}),
            labels=["Reynolds number", "e/D", "p/D"]).add(entry.pop.get("X")).do()
            Scatter(ax=ax2).add(entry.pop.get("F"), color='blue').do()
            #Scatter(ax=ax2).add(res.history[0].pop.get("F"), color='red').do()
            vid.record(fig=fig)
"""

## Best solution.
weights = [0.5,0.5]
Imin =  get_decomposition("asf").do(res.F, weights).argmin()
Imax =  get_decomposition("asf").do(res.F, weights).argmax()
plot=Scatter(figsize=(8,4), legend=True, tight_layout=True)
plot.add(res.F, color="grey", alpha=0.3, s=30)
plot.add(res.F[Imin], color="#ffaa00ff", s=30, label="max -Nu, min ff")
plot.add(res.F[Imax], color="black", s=30, label="min -Nu, max ff")
plot.do()
#plot.apply(lambda ax: ax.arrow(0, 0, 0.5, 0.5, color='black',
#                               head_width=0.01, head_length=0.01, alpha=0.4))
plot.show()



# Parallel chart plot
plot3 = PCP(show_bounds=False, n_ticks=5,labels="",
           legend=(True, {'loc': "upper left"}),
           tight_layout=True, figsize=(8,4)) #.add(entry.pop.get("X")).do()
plot3.add(dspace, color="grey", alpha=0.3)
plot3.add(res.X[Imin], color="#ffaa00ff", linewidth=3, label="max -Nu, min ff")
plot3.add(res.X[Imax], color="black", linewidth=3, label="min -Nu, max ff") ##b700ffff
plot3.show()



# Objective Space
plot2 = Scatter(title = "Objective Space", legend=True, tight_layout=True)
plot2.add(res.F, label="Pareto front", alpha=0.5) # res.F are objective space vlaues
plot2.add(res.history[0].pop.get("F"), label="Dominated solutions", alpha=0.5)
plot2.add(res.F[Imin], color="red", s=30, label="max -Nu, min ff")
plot2.add(res.F[Imax], color="black", s=30, label="min -Nu, max ff")
plot2.add(pf, plot_type="line", color="black", alpha=0.7)
plot2.show()

"""
#3D scatter plot
ps = problem.pareto_set(use_cache=False, flatten=False)
pf = problem.pareto_front(use_cache=False, flatten=False)

plot4 = Scatter(title = "Design Space", axis_labels="x")
plot4.add(res.X, s=30, facecolors='blue', edgecolors='r')
if ps is not None:
    plot4.add(ps, plot_type="line", color="black", alpha=0.7)
plot4.do()
plot4.show()
"""
