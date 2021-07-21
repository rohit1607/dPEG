import nashpy as nash
from game import deterministic_game
import pickle
import numpy as np
from utils import max_a1_min_a2, max_a2_min_a1, save_dict, get_solver_output_path, msne_utility



def Game_VI_onestep(game, Q_term):

    Q={}
    Q2={}
    policy = {}

    for s in game.non_term_S + game.term_S:
        Q[s] = np.zeros((game.n_A1, game.n_A2))
        Q2[s] = np.zeros((game.n_A1, game.n_A2))

    msne_util = {}
    # precompute msne utilites for Qnews
    for s in game.non_term_S:
        eq_list, utility_list = msne_utility(Q_term[s])
        try:
            msne_util[s] = utility_list[0]
            policy[s] = eq_list
        except:
            print("degen mat at s=",s)
            print("len(utility_list=", len(utility_list))

    for s in game.non_term_S:
        for a1 in game.A[0]:
            for a2 in game.A[1]:  
                try:
                    game.set_state(s)
                    old_Qsa = Q[s][a1,a2]
                    r, new_s = game.move(a1,a2)
                    Q[s][a1,a2] =  r + GAMMA*msne_util[new_s]
                except:
                    print("s,a1,a2, new_s= ", s,a1,a2, new_s)


    #     for s in game.non_term_S:
    #         for a1 in game.A[0]:
    #             for a2 in game.A[1]:  
    #                 try:
    #                     game.set_state(s)
    #                     old_Qsa = Q2[s][a1,a2]
    #                     r, new_s = game.move(a1,a2)
    #                     Q2[s][a1,a2] =  -r + GAMMA*max_a2_min_a1(Q2[new_s])
    #                     del_Q = abs(Q2[s][a1,a2] - old_Qsa)
    #                     del_Qsa_max = max(del_Qsa_max, del_Q)
    #                 except:
    #                     print("s,a1,a2, new_s= ", s,a1,a2, new_s)


    return Q, Q2, policy

def get_R_dict(game):
    R = {}
    for s in game.non_term_S + game.term_S:
        R[s] = np.zeros((game.n_A1, game.n_A2))
    for s in game.non_term_S:
        for a1 in game.A[0]:
            for a2 in game.A[1]:  
                try:
                    game.set_state(s)
                    r, new_s = game.move(a1,a2)
                    R[s][a1,a2] = r
                except:
                    print("s,a1,a2, new_s= ", s,a1,a2, new_s)
    return R


def solve_Game(game, nt):
    print("solving game with nt=", nt)
    Q_term = get_R_dict(game)
    full_policy = {}
    for t in range(nt):
        print("solving nt-",t+1)
        Q,_,policy = Game_VI_onestep(game,Q_term)
        Q_term = Q
        full_policy[t] = policy
    save_dict(full_policy, game.solver_output_path+"/full_policy.pkl")  
        
    paths_file = open("paths.txt","w")
    paths_file.write(game.solver_output_path)
    paths_file.close()

    save_dict(Q, game.solver_output_path+"/Q.pkl")
  
from input_data import *
solver_output_path = get_solver_output_path(method, gsize, nt, p1_startpos, p2_startpos, data_solverOutput_dir)
game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method, solver_output_path)
solve_Game(game, nt)