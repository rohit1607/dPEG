import nashpy as nash
from game import deterministic_game
import pickle
import numpy as np
from utils import max_min

from input_data import *
game = deterministic_game(gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method)

print(len(game.non_term_S), len(game.term_S))
R={}
Q={}
policy={}

print("building q[s] payoff matrices")
for s in game.non_term_S + game.term_S:
    Q[s] = np.zeros((game.n_A1, game.n_A2))
    # for a1 in game.A[0]:
    #     for a2 in game.A[1]:
    #         game.set_state(s)
    #         r, new_s = game.move(a1,a2)
    #         # print(s,a1,a2,new_s)
    #         R[s][a1,a2] = r
    # # print(q[s])
    # # policy[s] = nash.


count = 0
while True:
    count+=1
    del_Qsa_max = 0
    for s in game.non_term_S:
        for a1 in game.A[0]:
            for a2 in game.A[1]:  
                try:
                    game.set_state(s)
                    old_Qsa = Q[s][a1,a2]
                    r, new_s = game.move(a1,a2)
                    Q[s][a1,a2] =  r + GAMMA*max_min(Q[new_s])
                    del_Q = abs(Q[s][a1,a2] - old_Qsa)
                    del_Qsa_max = max(del_Qsa_max, del_Q)
                except:
                    print("s,a1,a2, new_s= ", s,a1,a2, new_s)
    print("count, del_Qsa_max= ", count, del_Qsa_max)

    if del_Qsa_max < 0.01:
        break


print("Computing policy")
for s in game.non_term_S:
    rps=nash.Game(Q[s], -Q[s])
    eqs = rps.support_enumeration()
    policy[s]= list(eqs)
    # print("policy=" ,s, policy[s], len(policy[s]))
    # if s == (1,0,1,3):
    #     break


policy_file = open("policy.pkl", "wb")
pickle.dump(policy, policy_file)
policy_file.close()

