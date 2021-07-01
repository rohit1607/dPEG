import numpy as np

class deterministic_game:
    def __init__(self, gsize, p1_startpos, p2_startpos, obstacle_mask, evader_targets):
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
        self.dxy = 0.5*abs(self.xs[1]-self.xs[0])

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
                        if (i1,j1)==(i2,j2):
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

    def rewards(self):
        return

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
            if self.is_outbound(p):
                self.i[p], self.j[p] = self.dynamics((self.i[p], self.j[p]), a[p], REVERSE=True)
                # print("outbound")
                if p==1:
                    r = -1
                if p==2:
                    r= +1

        if self.P_catches_E(s_old):
            r = +1
            # print("P_catches_E")

        if self.E_reaches_target():
            r = -1
            # print("E_reaches_target")

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