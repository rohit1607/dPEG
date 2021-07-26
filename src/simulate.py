from game import deterministic_game
import matplotlib.pyplot as plt
import numpy as np
import pickle
from scipy import stats
from os.path import join
from utils import manhattan, read_path_file


def manual_moves(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method):

    game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method)
    print(game.get_state(), game.s)
    print(game.move(2,1))
    print("-------")
    # game.set_state((1,1,1,1))
    # print(game.get_state(), game.s)
    # print(game.move(0,0))
    # print(game.move(1,3))
    # print(game.move(1,3))

def setup_grid_in_plot(fig, ax, g):

    msize = 100
    ax.set_xlim(-0.5,g.xs[-1] + (g.dxy/2))
    ax.set_ylim(-0.5,g.ys[-1] + (g.dxy/2))

    minor_ticks = [i + g.dxy/2 for i in range(0, gsize , 1)]
    major_ticks = [i for i in range(0, gsize , 1)]

    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticks(major_ticks, minor=False)
    ax.set_yticks(major_ticks, minor=False)
    ax.set_yticks(minor_ticks, minor=True)

    ax.grid(b= True, which='minor', color='#CCCCCC', axis='both',linestyle = '-', alpha = 0.5, zorder = -1e5)
    ax.tick_params(axis='both', which='both', labelsize=20)

    # ax.set_xlabel('X (Non-Dim)', fontsize = 20)
    # ax.set_ylabel('Y (Non-Dim)')

    p1_xy0 = g.ij_to_xy(g.p1_startpos)
    p2_xy0 = g.ij_to_xy(g.p2_startpos)
    # print("setting up grid with p1_xy0, p2_xy0= ", p1_xy0, p2_xy0)
    plt.scatter(p1_xy0[0], p1_xy0[1], marker = 'o', s = msize, color = 'k', zorder = 1e5)
    plt.scatter(p2_xy0[0], p2_xy0[1], marker = '^', s = msize, color = 'k', zorder = 1e5)
    for targ in g.ev_targs:
        xtarg, ytarg = g.ij_to_xy(targ)
        plt.scatter(xtarg, ytarg, marker = 'x', s = 3*msize, color = 'k', zorder = 1e5)
    for i in range(g.gsize):
        for j in range(g.gsize):
            if g.obs_mask[i,j] == 1:
                obs_xy = g.ij_to_xy((i,j))
                plt.scatter(obs_xy[0], obs_xy[1], marker = 's',s = 10*msize,color ='c')
    # x_ssg, y_ssg =  get_sg_square_corners(g, 'start')
    # plt.fill(x_ssg, y_ssg, 'g', alpha = 0.5, zorder = 0)
    # if (0<= g.endpos[0] < gsize) and (0<= g.endpos[1] < gsize):
    #     plt.scatter(g.xs[g.endpos[1]], g.ys[g.ni - 1 - g.endpos[0]], marker = '*', s = msize*2, color ='k', zorder = 1e5)
    #     x_tsg, y_tsg =  get_sg_square_corners(g, 'target')
    #     plt.fill(x_tsg, y_tsg, 'r', alpha = 0.5, zorder = 0)

    plt.gca().set_aspect('equal', adjustable='box')

def sample_action(d_a1):

    xk = np.arange(len(d_a1))
    pk = d_a1
    distr = stats.rv_discrete(name='custm', values=(xk, pk))
    return int(distr.rvs(size=1)[0])


def generate_trajectories(g, policy):

    traj = []
    s = g.get_state()
    traj.append(s)

    count = 0
    while True:
        count+=1
        print("s=",s, len(policy[s]))
        id = np.random.randint(0,len(policy[s]),1)[0]
        print("id=", id)
        d_a = policy[s][id]
        a1 = sample_action(d_a[0])
        a2 = sample_action(d_a[1])
        print(d_a, a1, a2)
        r, s = g.move(a1, a2)
        traj.append(s)
        if s in g.term_S or count>=MAX_SIM_ITERS:
            break
        
    return traj

def plot_trajectories(g, traj, policy, fname=None):



    p1_xtr = []
    p1_ytr = []
    p2_xtr = []
    p2_ytr = []
    for t in range(len(traj)):
        s =  traj[t]
        x1, y1 = g.ij_to_xy((s[0],s[1]))
        x2, y2 = g.ij_to_xy((s[2],s[3]))

        p1_xtr.append(x1)
        p1_ytr.append(y1)
        p2_xtr.append(x2)
        p2_ytr.append(y2)

    for t in range(len(traj)):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        setup_grid_in_plot(fig, ax, g)
        # annotations = [i for i in range(t) ]
        try:
            print("t=", t)
            plt.plot(p1_xtr[0:t+1], p1_ytr[0:t+1], color='r',label='Pursuer')
            plt.scatter(p1_xtr[0:t+1], p1_ytr[0:t+1], color='r')
            plt.plot(p2_xtr[0:t+1], p2_ytr[0:t+1], color='g', label='Evader')
            plt.scatter(p2_xtr[0:t+1], p2_ytr[0:t+1], marker='^', color='g')

            plt.annotate(str(t), (p1_xtr[t], p1_ytr[t]),color='r')
            plt.annotate(str(t), (p2_xtr[t], p2_ytr[t]), color='g')
            plt.legend()
        except:
            assert(0>1)

        
        imgname = fname +"@t" +str(t)
        # filename = join(plot_seq_path, fname) + "@t" + str(t) + ".png"
        plt.savefig(imgname, bbox_inches = "tight", dpi = 300)
        plt.clf()
        plt.close()

    return

def check_policy(policy):
    print("states with 0 length policies")
    for s in policy.keys():
        if len(policy[s]) == 0:
            print(s, manhattan((s[0],s[1]),(s[2],s[3])))

from input_data import *

# p1_startpos = (0,0)
# p2_startpos = (1,1)

# p1_startpos = (1,1)
# p2_startpos = (0,0)

# p1_startpos = (2,2)
# p2_startpos = (0,0)

# p1_startpos = (0,0)
# p2_startpos = (1,3)

# p1_startpos = (0,0)
# p2_startpos = (0,5) #(0,5), (0,7), (5,6), (7,0)

# p1_startpos = (1,0)
# p2_startpos = (0,2) 
solver_output_path = read_path_file()
game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method, solver_output_path)

# manual_moves(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets)


print("path=", solver_output_path)

policy_file = open(solver_output_path+"/policy.pkl", "rb")
policy = pickle.load(policy_file)
policy_file.close()
check_policy(policy)

fname=solver_output_path+"/traj"
print("fname=",fname)
traj = generate_trajectories(game, policy)
print("traj= ", traj)
plot_trajectories(game, traj, policy, fname)
# plt.show()

