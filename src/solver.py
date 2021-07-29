import nashpy as nash
from game import deterministic_game
import pickle
import numpy as np
from utils import max_a1_min_a2, max_a2_min_a1, save_dict, get_solver_output_path, msne_utility

from input_data import *


def Game_VI(game):

    print(len(game.non_term_S), len(game.term_S))
    R={}
    Q={}
    Q2={}

    print("building q[s] payoff matrices")
    for s in game.non_term_S + game.term_S:
        Q[s] = np.zeros((game.n_A1, game.n_A2))
        Q2[s] = np.zeros((game.n_A1, game.n_A2))

    msne_util = {}
    count = 0
    while True:
        count+=1
        del_Qsa_max = 0
            # TODO: precompute msne utilites for Qnews
        for s in game.non_term_S:
            eq_list, utility_list = msne_utility(Q[s])
            try:
                msne_util[s] = utility_list[0]
            except:
                print("degen mat at s=",s)
                print("len(utility_list=", len(utility_list))

        for s in game.term_S:
            msne_util[s]= 0
            
        for s in game.non_term_S:
            for a1 in game.A[0]:
                for a2 in game.A[1]:  
                    try:
                        game.set_state(s)
                        old_Qsa = Q[s][a1,a2]
                        r, new_s = game.move(a1,a2)
                        Q[s][a1,a2] =  r + GAMMA*msne_util[new_s]
                        del_Q = abs(Q[s][a1,a2] - old_Qsa)
                        del_Qsa_max = max(del_Qsa_max, del_Q)
                    except:
                        print("s,a1,a2, new_s= ", s,a1,a2, new_s)
        print("count, del_Qsa_max= ", count, del_Qsa_max)

        if del_Qsa_max < TOL:
            break

    # count = 0
    # while True:
    #     count+=1
    #     del_Qsa_max = 0
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
    #     print("count, del_Qsa_max= ", count, del_Qsa_max)

    #     if del_Qsa_max < TOL:
    #         break

    return Q, Q2

def compute_Game_Policy(game,Q,checklist=None):
    policy={}
    eQ = {}     
    for s in game.non_term_S:
        eQ[s] = -Q[s]
        rps=nash.Game(Q[s], eQ[s])
        eqs = rps.support_enumeration()
        policy[s]= list(eqs)
        if checklist != None:
            if s in checklist:
                print("Q[s]=\n", Q[s])
                print("policy=" ,s, policy[s], len(policy[s]))
                print()
        # if s == (1,0,1,3):
        #     break
    return policy





def solve_Game(game):

    Q,Q2 = Game_VI(game)
    paths_file = open("paths.txt","w")
    paths_file.write(game.solver_output_path)
    paths_file.close()

    save_dict(Q, game.solver_output_path+"/Q.pkl")

    save_dict(Q2, game.solver_output_path+"/Q2.pkl")

    checklist = [(1,2,0,3),
                (2,1,3,0),
                (2,2,3,3) ]

    print("Computing policy")
    policy = compute_Game_Policy(game,Q,checklist)
    save_dict(policy, game.solver_output_path+"/policy.pkl")    


solver_output_path = get_solver_output_path(method, gsize, p1_startpos, p2_startpos, data_solverOutput_dir)
game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method, solver_output_path)
solve_Game(game)