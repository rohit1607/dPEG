from game import deterministic_game
import matplotlib.pyplot as plt
import numpy as np
import pickle


def manual_moves(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets):

    game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets)
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
    ax.set_xlim(0,g.xs[-1] + (g.dxy/2))
    ax.set_ylim(0,g.ys[-1] + (g.dxy/2))

    minor_ticks = [i-g.dxy for i in range(0, gsize + 1, gsize)]
    major_ticks = [i-g.dxy for i in range(0, gsize + 1, gsize)]

    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticks(major_ticks, minor=False)
    ax.set_yticks(major_ticks, minor=False)
    ax.set_yticks(minor_ticks, minor=True)

    # ax.grid(b= True, which='both', color='#CCCCCC', axis='both',linestyle = '-', alpha = 0.5, zorder = -1e5)
    ax.tick_params(axis='both', which='both', labelsize=20)

    # ax.set_xlabel('X (Non-Dim)', fontsize = 20)
    # ax.set_ylabel('Y (Non-Dim)')

    p1_xy0 = g.ij_to_xy(g.p1_startpos)
    p2_xy0 = g.ij_to_xy(g.p2_startpos)
    print("p1_xy0, p2_xy0= ", p1_xy0, p2_xy0)
    plt.scatter(p1_xy0[0], p1_xy0[1], marker = 'o', s = msize, color = 'k', zorder = 1e5)
    plt.scatter(p2_xy0[0], p2_xy0[1], marker = '^', s = msize, color = 'k', zorder = 1e5)
    for targ in g.ev_targs:
        xtarg, ytarg = g.ij_to_xy(targ)
        plt.scatter(xtarg, ytarg, marker = 'x', s = 3*msize, color = 'k', zorder = 1e5)
    # x_ssg, y_ssg =  get_sg_square_corners(g, 'start')
    # plt.fill(x_ssg, y_ssg, 'g', alpha = 0.5, zorder = 0)
    # if (0<= g.endpos[0] < gsize) and (0<= g.endpos[1] < gsize):
    #     plt.scatter(g.xs[g.endpos[1]], g.ys[g.ni - 1 - g.endpos[0]], marker = '*', s = msize*2, color ='k', zorder = 1e5)
    #     x_tsg, y_tsg =  get_sg_square_corners(g, 'target')
    #     plt.fill(x_tsg, y_tsg, 'r', alpha = 0.5, zorder = 0)

    plt.gca().set_aspect('equal', adjustable='box')


def plot_trajectories(g, policy):

    # while True:
    s = g.get_state()
    print("s=",s)
    a = policy[s]
    print(a)


GAMMA=0.9
gsize = 4
p1_startpos = (0,0)
p2_startpos = (3,3)
obstacle_mask = np.zeros((gsize,gsize))
evader_targets = [(3,1)]
game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets)

# manual_moves(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets)


policy_file = open("policy.pkl", "rb")
policy = pickle.load(policy_file)
policy_file.close()


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1)
setup_grid_in_plot(fig, ax, game)
plot_trajectories(game, policy)
# plt.show()