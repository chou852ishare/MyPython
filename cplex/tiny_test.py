#!/usr/bin/python

import numpy as np
import cplex
from cplex.exceptions import CplexError
import sys


# constants
N   = 60000   # number of nodes in network
T   = 10      # time horizon
S   = 1       # |seed set|
M   = 100     # big M
UB  = 100     # upper bound of variables


# generate adjacency matrix
w = np.zeros((N, N))
# star-like network
w[0] = np.ones(N) * 0.8
w[0][0] = 0
# chain network
#for i in xrange(N-1):
#    w[i][i+1] = 1 * 0.7

# objective and constraint coefficients
im_obj_t    = np.ones(N*T).tolist()
im_obj_0    = np.ones(N).tolist()
im_ub       = (UB * np.ones(N*T)).tolist()
im_rhs      = np.concatenate((np.zeros(N*T), M*np.ones(N*T), S*np.ones(1))).tolist()
im_sense    = 'L' * (2*N*T+1)


# sparse constraint matrix
# basic indices and values
ind_w   = np.nonzero(-w.T)
val_w   = (-w.T)[ind_w]
ind_I   = (np.arange(N), np.arange(N))
val_I   = np.ones(N)
# extend
ind0    = np.array([])
ind1    = np.array([])
val     = np.array([])
for t in xrange(T):
    # nonzero coefficients of w
    ind0    = np.concatenate((ind0, ind_w[0]+t*N))
    ind1    = np.concatenate((ind1, ind_w[1]+t*N))
    val     = np.concatenate((val, val_w))
    # nonzero coefficients of I in c2
    ind0    = np.concatenate((ind0, ind_I[0]+t*N))
    ind1    = np.concatenate((ind1, ind_I[1]+(t+1)*N))
    val     = np.concatenate((val, val_I))
    # nonzero coefficients of MI
    ind0    = np.concatenate((ind0, ind_I[0]+(t+T)*N))
    ind1    = np.concatenate((ind1, ind_I[1]))
    val     = np.concatenate((val, val_I*M))
    # nonzero coefficients of I in c3
    ind0    = np.concatenate((ind0, ind_I[0]+(t+T)*N))
    ind1    = np.concatenate((ind1, ind_I[1]+(t+1)*N))
    val     = np.concatenate((val, val_I))
ind0 = (np.concatenate((ind0, np.ones(N)*(2*N*T)))).astype(int).tolist()
ind1 = (np.concatenate((ind1, np.arange(N)))).astype(int).tolist()
val  = (np.concatenate((val, np.ones(N)))).tolist()
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

