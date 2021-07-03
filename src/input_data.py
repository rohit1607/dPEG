import numpy as np

GAMMA=0.9
MAX_SIM_ITERS = 30

gsize = 4
p1_startpos = (0,0)
p2_startpos = (3,3)
obstacle_mask = np.zeros((gsize,gsize))
evader_targets = [(3,1)]