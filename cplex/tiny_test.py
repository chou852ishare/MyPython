#!/usr/bin/python

import cplex
from cplex.exceptions import CplexError
import sys

# data common to all populateby functions
my_obj      = [1.0, 2.0, 3.0]
my_ub       = [40.0, cplex.infinity, cplex.infinity]
my_rhs      = [20.0, 30.0]
my_sense    = "LL"


def populatebyrow(prob):
    prob.objective.set_sense(prob.objective.sense.maximize)

    # since lower bounds are all 0.0 (the default), lb is omitted here
    prob.variables.add(obj = my_obj, ub = my_ub, names = my_colnames)

    # can query variables like the following:

    # lbs is a list of all the lower bounds
    lbs = prob.variables.get_lower_bounds()

    # ub1 is just the first lower bound
    ub1 = prob.variables.get_upper_bounds(0) 

    # names is ["x1", "x3"]
    names = prob.variables.get_names([0, 2])

    rows = [[[0,"x2","x3"],[-1.0, 1.0,1.0]],
            [["x1",1,2],[ 1.0,-3.0,1.0]]]

    prob.linear_constraints.add(lin_expr = rows, senses = my_sense,
                                rhs = my_rhs, names = my_rownames)

    # because there are two arguments, they are taken to specify a range
    # thus, cols is the entire constraint matrix as a list of column vectors
    cols = prob.variables.get_cols("x1", "x3")

    
def populatebynonzero(prob):
    prob.objective.set_sense(prob.objective.sense.maximize)
    
    prob.linear_constraints.add(rhs = my_rhs, senses = my_sense,
                                names = my_rownames)
    prob.variables.add(obj = my_obj, ub = my_ub, names = my_colnames)
    
    rows = [0,0,0,1,1,1]
    cols = [0,1,2,0,1,2]
    vals = [-1.0,1.0,1.0,1.0,-3.0,1.0]
    
    prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
    
    
def lpex1():
    try:
        my_prob = cplex.Cplex()
        
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


if __name__ == "__main__":
    lpex1()

