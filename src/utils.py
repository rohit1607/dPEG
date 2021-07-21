
import pickle
import os
from pathlib import Path
import nashpy as nash


def max_a1_min_a2(mat):
    m,n = mat.shape
    return max([min(mat[i,:]) for i in range(m)])

def max_a2_min_a1(mat):
    m,n = mat.shape
    return max([min(mat[:,j]) for j in range(n)])

def msne_utility(mat):
    m,n = mat.shape
    game = nash.Game(mat, -mat)
    equilibria = game.support_enumeration()
    # print("INF eqs=",list(equilibria))
    utility_list = []
    eq_list = []
    for eq in equilibria:
        # print("eq=",eq)
        sigma1, sigma2 = eq
        # print("sigma1=", sigma1)
        # print("sigma2=", sigma2)
        utility = game[sigma1, sigma2]
        # print("utility=", utility)
        utility_list.append(utility[0])
        eq_list.append(eq)

    return eq_list, utility_list

# import numpy as np
# A = np.arange(16).reshape((4,4))
# print(A, max_min(A))

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def check_policy(policy):
    print("states with 0 length policies")
    for s in policy.keys():
        if len(policy[s]) == 0:
            print(s)

def read_path_file():
    path_file=open("paths.txt","r")
    return path_file.readline()

def save_dict(dict, fpath_fname):
    dict_file = open(fpath_fname,"wb")
    pickle.dump(dict, dict_file)
    dict_file.close()

def get_solver_output_path(method, gsize, p1_startpos, p2_startpos, data_solverOutput_dir):
    tmp_prob_name=method + "_g" + str(gsize) + "_p" + str(p1_startpos) + "_" +str(p2_startpos)
    solver_output_path = os.path.join(data_solverOutput_dir, tmp_prob_name)
    print(solver_output_path)
    try:
        Path(solver_output_path).mkdir(parents=False, exist_ok=False)
    except:
        for t in range(1,20):
            new_solver_output_path = solver_output_path + "_" + str(t)
            try:
                Path(new_solver_output_path).mkdir(parents=False, exist_ok=False)
                break
            except:
                pass
        solver_output_path = new_solver_output_path
        
    return solver_output_path