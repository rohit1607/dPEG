import pickle
import nashpy as nash
import numpy as np
import pickle
from utils import read_path_file

# A = np.array( [[ -0.95,        -1.  ,        33. ,         -1.   ,       31.05      ],
#             [ -1.  ,        -0.95  ,      -0.95   ,     -1.05   ,     31.        ],
#             [ -1.   ,       -1.84819815,  -0.95    ,    -1.05,        31.        ],
#             [ -1.,         -26.2592,     -26.0642,      -0.95,        31.        ],
#             [ 33.,         -26.0642,       5.9358,      -0.95,        33.        ]] )

# rps=nash.Game(A, -A)
# eqs = rps.support_enumeration()
# print(list(eqs))

path = read_path_file()
Q_file = open(path+"/Q.pkl", "rb")
Q1 = pickle.load(Q_file)
Q_file.close()

Q2_file = open(path+"/Q2.pkl", "rb")
Q2 = pickle.load(Q2_file)
Q2_file.close()

def compare_Q1_Q2(Q1,Q2):
    count=0
    for s in Q1.keys():
        # print(Q1[s])
        # print(Q2[s])
        # if not np.all(Q1[s] == -Q2[s]):
        #     print(s)
        #     print(Q1[s])
        #     print(Q2[s])
        if np.linalg.norm(Q1[s]+Q2[s], ord='fro') > 0.1:
            # print(s, Q1[s]+Q2[s])
            count+=1
        else:
            print(s, Q1[s]+Q2[s])
    print(count)


compare_Q1_Q2(Q1, Q2)
