import numpy as np

GAMMA=0.95
MAX_SIM_ITERS = 30

gsize = 4
p1_startpos = (1,1)
p2_startpos = (0,0)
obstacle_mask = np.zeros((gsize,gsize))
evader_targets = [(3,1)]
# methods= ['r_term_only','del_t','final_manh','del_manh']
method = 'del_manh'

