import numpy as np
import os
# from pathlib import Path
project_root_path = os.path.abspath(os.pardir)
project_root_path = os.path.abspath(os.pardir)
data_solverOutput_dir = os.path.join(project_root_path, "data_solverOutput")


GAMMA=0.95
MAX_SIM_ITERS = 30
TOL = 0.01
gsize = 4
p1_startpos = (0,0)
p2_startpos = (3,0)
obstacle_mask = np.zeros((gsize,gsize))
# obs_list = [(5,3),(4,3),(3,3)]
obs_list = [(1,1)]
for obs in obs_list:
    i,j = obs
    obstacle_mask[i,j]=1
evader_targets = [(2,3)]
# methods= ['r_term_only','del_t','final_manh','del_manh']
method = 'del_manh'

