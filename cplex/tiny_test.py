#!/usr/bin/python

import numpy as np
import cplex
from cplex.exceptions import CplexError
import sys


# constants
N   = 60000  # number of nodes in network
T   = 10      # time horizon
S   = 1       # |seed set|
M   = 100     # big M
UB  = 100     # upper bound of variables


# generate adjacency matrix
# star-like network
#w_to    = range(1, N) # -w.T
#w_fr    = [0] * (N-1)
#w_val   = [-0.8] * (N-1)
# chain network
w_to     = range(1, N)
w_fr     = range(0, N-1)
w_val    = [-0.8] * (N-1)


# objective and constraint coefficients
im_obj_t    = [1] * (N*T)
im_obj_0    = [1] * N
im_ub       = [UB] * (N*T)
im_rhs      = [0]*(N*T) + [M]*(N*T) + [S]
im_sense    = 'L' * (2*N*T+1)


# sparse constraint matrix
# basic indices and values
ind_w   = (w_to, w_fr)
val_w   = w_val
ind_I   = (range(N), range(N))
val_I   = [1] * N
val_M   = [M] * N
# extend
ind0    = []
ind1    = []
val     = []
for t in xrange(T):
    # nonzero coefficients of w
    ind0.extend([x+t*N for x in ind_w[0]])
    ind1.extend([x+t*N for x in ind_w[1]])
    val.extend(val_w)
    # nonzero coefficients of I in c2
    ind0.extend([x+t*N for x in ind_I[0]])
    ind1.extend([x+(t+1)*N for x in ind_I[1]])
    val.extend(val_I)
    # nonzero coefficients of MI
    ind0.extend([x+(t+T)*N for x in ind_I[0]])
    ind1.extend(ind_I[1])
    val.extend(val_M)
    # nonzero coefficients of I in c3
    ind0.extend([x+(t+T)*N for x in ind_I[0]])
    ind1.extend([x+(t+1)*N for x in ind_I[1]])
    val.extend(val_I)
ind0.extend([2*N*T] * N)
ind1.extend(range(N))
val.extend([1] * N)
print len(ind0), len(ind1), len(val)


def populatebyrow(prob):
    prob.objective.set_sense(prob.objective.sense.maximize)
    # lower bounds are all 0.0 (the default)
    # xi0 is binary
    # xit is continuous for t >= 1
    prob.variables.add(obj = im_obj_t, ub = im_ub)
    prob.variables.add(obj = im_obj_0, types = prob.variables.type.binary * N)
    rows = [[range(N*(T+1)), a.tolist()] for a in c[:]]
    prob.linear_constraints.add(lin_expr = rows, senses = im_sense, rhs = im_rhs)

    
def populatebynonzero(prob):
    prob.objective.set_sense(prob.objective.sense.maximize)
    # lower bounds are all 0.0 (the default)
    # xi0 is binary
    # xit is continuous for t >= 1
    prob.variables.add(obj = im_obj_0, types = prob.variables.type.binary * N)
    prob.variables.add(obj = im_obj_t, ub = im_ub)
    prob.linear_constraints.add(senses = im_sense, rhs = im_rhs)
    prob.linear_constraints.set_coefficients(zip(ind0, ind1, val))
   

def lpex1():
    try:
        my_prob = cplex.Cplex()
        pop_method = 'n'
        if pop_method == "r":
            handle = populatebyrow(my_prob)
        if pop_method == "n":
            handle = populatebynonzero(my_prob)
        my_prob.solve()
    except CplexError, exc:
        print exc
        return

    print
    # solution.get_status() returns an integer code
    print "Solution status = " , my_prob.solution.get_status(), ":",
    # the following line prints the corresponding string
    print my_prob.solution.status[my_prob.solution.get_status()]
    print "Solution value  = ", my_prob.solution.get_objective_value()
    x     = my_prob.solution.get_values()
    x     = np.reshape(x, (T+1, N))
    print "Solution variables = ", x


if __name__ == "__main__":
    lpex1()

