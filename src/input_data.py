import numpy as np
import os
from utils import load_vel_field
# from pathlib import Path
project_root_path = os.path.abspath(os.pardir)
project_root_path = os.path.abspath(os.pardir)
data_solverOutput_dir = os.path.join(project_root_path, "data_solverOutput")
data_Input_dir = os.path.join(project_root_path, "data_Input")

GAMMA=0.95
MAX_SIM_ITERS = 30
TOL = 0.01

gsize = 4
nt = 5

p1_startpos = (0,0)
p2_startpos = (3,0)

obstacle_mask = np.zeros((gsize,gsize))
# obs_list = [(5,3),(4,3),(3,3)]
obs_list = [(1,1)]
for obs in obs_list:
    i,j = obs
    obstacle_mask[i,j]=1


evader_targets = [(3,3)]
# methods= ['r_term_only','del_t','final_manh','del_manh']
method = 'del_t'

env_name = 'g4_nt5_half_flow'
full_env_path = os.path.join(data_Input_dir,env_name)
env = {}
env['velx'], env['vely'], env['nrzns'], env['nt'] = load_vel_field(full_env_path)