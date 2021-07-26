import numpy as np
from numpy.lib.function_base import sort_complex
from utils import manhattan, save_dict




class deterministic_game:
    def __init__(self, gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets, method, solver_output_path):
        """
        gsize: int
        p1_startpos: (int, int)
        p2_ .. . .
        obstacle_mask: ndarray of size gsize x gsize with 0 or 1
        evader_targets: [(e_i, e_j), (int, int), .. ]
        """
        # TODO: 1. Put asserts to check if startpos and evader_targets are inside grid

        self.gsize = gsize
        self.ncells = gsize*gsize
        self.i = {}
        self.j = {}
        self.p1_startpos = p1_startpos
        self.p2_startpos = p2_startpos
        self.i[1], self.j[1] = p1_startpos
        self.i[2], self.j[2] = p2_startpos
        self.s = (self.i[1], self.j[1], self.i[2], self.j[2])
        self.obs_mask = obstacle_mask
        self.ev_targs = evader_targets
        self.states()
        self.actions()
        self.xs = [i for i in range(gsize)]
        self.ys = [j for j in range(gsize)]
        self.dxy = abs(self.xs[1]-self.xs[0])
        self.r_term = 4*gsize
        self.method = method
        self.opt_measure = None
        self.solver_output_path = solver_output_path
        if not np.all(self.obs_mask == 0):
            print("obstacle present")
            self.solve_MDPs_for_optimal_measures()


    def set_solver_output_path(self, path):
        self.solver_output_path = path

    def states(self):
        gsize = self.gsize
        # self.S = []
        self.term_S = []
        self.non_term_S = []
        for i1 in range(gsize):
            for j1 in range(gsize):
                for i2 in range(gsize):
                    for j2 in range(gsize):
                        # self.S.append((i1,j1,i2,j2))
                        # TODO: add obstacle barged-in cases to termS 
                        if (i1,j1)==(i2,j2) or (i2,j2) in self.ev_targs or self.obs_mask[i1,j1]==1 or self.obs_mask[i2,j2]==1:
                            self.term_S.append((i1,j1,i2,j2))
                        else:
                            self.non_term_S.append((i1,j1,i2,j2))

    def actions(self):
        # 0: nothing, 1: right, 2: down, 3: left, 4: up
        self.n_A1 = 5
        self.n_A2 = 5
        self.A1 = [i for i in range(self.n_A1)]
        self.A2 = [i for i in range(self.n_A2)]
        self.A = [self.A1, self.A2]


    def dynamics(self, pos, a, REVERSE=False):
        """
        pos: (int, int)
        a: action
        """
        i,j = pos

        if not REVERSE:
            if a == 0:
                pass
            # right
            if a == 1:
                j += 1
            # down
            if a == 2:
                i += 1
            # left
            if a == 3:
                j -= 1
            # up
            if a == 4:
                i -= 1

        if REVERSE:
            if a == 0:
                pass
            if a == 1:
                j -= 1
            if a == 2:
                i -= 1
            if a == 3:
                j += 1
            if a == 4:
                i += 1     
            
        return i,j

    def solve_MDPs_for_optimal_measures(self):
        self.opt_measure={}
        for i2 in range(self.gsize):
            for j2 in range(self.gsize):
                if self.obs_mask[i2,j2]==0:
                    V = self.solve_MDP((i2,j2))
                    fname=self.solver_output_path+ "/V"+str((i2,j2))
                    save_dict(V,fname)
                for i1 in range(self.gsize):
                    for j1 in range(self.gsize):
                        if self.obs_mask[i1,j1]==0:
                            self.opt_measure[(i1,j1),(i2,j2)] = V[(i1,j1)]
        return

    def solve_MDP(self, s2):
        V = {}
        for i1 in range(self.gsize):
            for j1 in range(self.gsize):
                if self.obs_mask[i1,j1]==0:
                    V[(i1,j1)]=0

        count = 0
        while True:
            count+=1
            del_Vs_max = 0
            for i1 in range(self.gsize):
                for j1 in range(self.gsize):
                    if self.obs_mask[i1,j1]==0:
                        Vs = -np.inf
                        for a1 in self.A[0]: 
                            # try:
                            s = (i1,j1)
                            old_Vs = V[s]
                            r, new_s = self.mdp_move(s, a1, s_term=s2)
                            tempV = r + V[new_s]
                            if tempV > Vs:
                                Vs = tempV
                            # except:
                            #     print("MDP exceptoin: s,a1, new_s, s2= ", s,a1, new_s, s2)

                        V[s] = Vs
                        del_V = abs(V[s] - old_Vs)
                        del_V_max = max(del_Vs_max, del_V)

            if del_V_max < 0.01:
                print("count, del_Vs_max= ", count, del_Vs_max)
                break
        return V

    def mdp_move(self, s, a1, s_term):
        r = -1
        i_pr, j_pr = self.dynamics(s,a1)
        # print("s, a1,s_term, i_pr, j_pr, = ", s,a1,s_term, i_pr, j_pr)
        new_s = (i_pr, j_pr)
        if not((0 <= i_pr < self.gsize) and (0 <= j_pr < self.gsize)):
            r = -100
            new_s = s
        elif((self.obs_mask[i_pr,j_pr]==1)):
            r = -100
            new_s = s
        elif s_term == new_s:
            r = 0
        return r, new_s

    def general_one_step_rewards(self, s_old):
        r = 0

        if self.method == 'r_term_only':
            pass

        if self.method == 'del_t':
            r = -1

        # TODO: manhattan distance to take into account obstacles
        if self.method == 'del_manh':
            if np.all(self.obs_mask==0):
                # print("no obstacles")
                r = -(manhattan((self.i[1],self.j[1]),(self.i[2],self.j[2])) 
                    - manhattan((s_old[0], s_old[1]),(s_old[2], s_old[3]))  )
            else:
                r = (self.opt_measure[(self.i[1],self.j[1]),(self.i[2],self.j[2])] 
                    - self.opt_measure[(s_old[0], s_old[1]),(s_old[2], s_old[3])]  )

        
        if self.method == 'final_manh':
            r = -manhattan((self.i[1],self.j[1]),(self.i[2],self.j[2]))
        

        return r

    # def mdp_move()

    def move(self, a1, a2):
        """
        p: 1 or 2 (player number)
        a: action
        """
        # assert(p==1 or p==2)
        assert((a1 in self.A1) and (a2 in self.A2))

        # Temp dictionary of player actions
        a = {}
        a[1] = a1
        a[2] = a2

        # Temp var storing one-step reward for pursuer, player 1. 
        # For player 2, the one-step reward is just the negative of that of p1
        r = 0

        # temp vars to store state
        s_old = self.get_state()

        # Both player perform actions
        for p in [1,2]:
            # if player is in interior, move as per action, else don't move (or do action 0)
            if not (self.in_obstacle(p) or self.is_outbound(p)):
                self.i[p], self.j[p] = self.dynamics(self.get_pos(p), a[p])
            else:
                self.i[p], self.j[p] = self.dynamics(self.get_pos(p), 0)

            # if player goes outbound after making the move, reverse the move
            if self.is_outbound(p) or self.obs_mask[self.i[p],self.j[p]]==1:
                self.i[p], self.j[p] = self.dynamics((self.i[p], self.j[p]), a[p], REVERSE=True)
                # print("outbound")
                if p==1:
                    r = -self.r_term
                if p==2:
                    r= +self.r_term
        
        if self.P_catches_E(s_old):
            r = +self.r_term
            # print("P_catches_E")

        if self.E_reaches_target():
            r = -self.r_term
            # print("E_reaches_target")

        # add general one step reward based on method 
        r += self.general_one_step_rewards(s_old)

        self.set_state((self.i[1], self.j[1], self.i[2], self.j[2]))

        return r, self.get_state()


    def P_catches_E(self, s_old):
        # if both players are in same position and not in an obstacle
        i1, j1, i2, j2 = s_old
        if ((self.i[1], self.j[1]) == (self.i[2], self.j[2])) and not self.in_obstacle(1):
            return True
        # to account players going through each other as a capture
        elif (i1,j1)==(self.i[2],self.j[2]) and (i2,j2)==(self.i[1],self.j[1]):
            return True
        else:
            return False
        

    def E_reaches_target(self):
        if (self.i[2], self.j[2]) in self.ev_targs:
            return True
        else:
            return False

    def in_obstacle(self, p):
        i,j = self.get_pos(p)
        if self.obs_mask[i,j]==1:
            return True
        else:
            return False
    
    def is_outbound(self, p):
        i,j = self.i[p], self.j[p]
        # print(p,i,j)
        if not ((0 <= i < self.gsize) and (0 <= j < self.gsize)):
            return True
        else:
            return False
        

    def get_pos(self, p):
        if p==1:
            return (self.s[0], self.s[1])
        if p==2:
            return (self.s[2], self.s[3])

    def get_state(self):
        return self.s

    def get_actions(self, p):
        assert(p==1 or p==2)
        if p == 1:
            return self.A1
        if p == 2:
            return self.A2

    # def get_states(self):
    #     return self.S

    def set_state(self, s):
        """
        s: (self.i[1], self.j[1], self.i[2], self.j[2])
        """
        self.s = s

    def ij_to_xy(self, pos):
        i, j = pos
        x = j
        y = self.gsize - i - 1
        return (x,y)