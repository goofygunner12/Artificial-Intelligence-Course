import numpy as np
import sys
import time
import timeit
import simplex as s


def run_test_single(test_id, primal, simplex_method):
    data=np.load('test_cases/test{0}.npz'.format(test_id))
    I,I_dual,A,b,c,f,x = data['I'], data['I_dual'], data['A'], data['b'], data['c'], data['f'], data['x']

    if primal:
        f1,x1 = simplex_method(I, c, A, b)
    else:
        f1,x1 = simplex_method(I_dual, c, A, b)


    if np.linalg.norm(x1 - x) < 1e-10:
        print "Passed test case {0}".format(test_id)
    else:
        print  "Failed test case {0}".format(test_id)


def run_test_compare(test_id):
    data=np.load('test_cases/test{0}.npz'.format(test_id))
    I,I_dual,A,b,c,f,x = data['I'], data['I_dual'], data['A'], data['b'], data['c'], data['f'], data['x']

    start = time.time()
    s.simplex(I, c, A, b)
    simplex_time = time.time() - start
    start = time.time()
    s.revised_simplex(I, c, A, b)
    revised_time = time.time() - start

    print 'Simplex time: ', simplex_time
    print 'Revised time: ', revised_time

def add_constraint_test(test_id):
    data=np.load('test_cases/test{0}.npz'.format(test_id))
    I,I_dual,A,b,c,g,h,f,x = data['I'], data['I_dual'], data['A'], data['b'], data['c'], data['g'], data['h'], data['f'], data['x']

    f1,x1 = s.add_constraint(I_dual, c, A, b, g, h)


    if np.linalg.norm(x1 - x) < 1e-10:
        print "Passed test case {0}".format(test_id)
    else:
        print  "Failed test case {0}".format(test_id)


def test_simplex(I, c, A, b):
    s.simplex(I, c, A, b)

def test_revised_simplex(I, c, A, b):
    s.revised_simplex(I, c, A, b)

def run_test_compare2(test_id):
    setup = '''
import numpy as np
import simplex as s

data=np.load('test_cases/test{0}.npz'.format({0}))
I,A,b,c,f,x = data['I'], data['A'], data['b'], data['c'], data['f'], data['x']
'''.format(test_id)

    t1 = timeit.Timer('s.simplex(I, c, A, b)', setup)
    t2 = timeit.Timer('s.revised_simplex(I, c, A, b)', setup)

    print 'Simplex time: ', t1.timeit(1)
    print 'Revised time: ', t2.timeit(1)
    print
if len(sys.argv) == 1:
    print "\n\n\tSelect method to test with:"
    print "\tpython test.py test"
    print "\twhere test can be: simplex, revised, dual, compare_time, add_constraint\n\n"

    print "\n\tsimplex, revised, and dual test whether the \n\tcorresponding algorithm returns the right answer"
    print "\n\tcompare_time prints out the timings of your \n\tsimplex and revised simplex algorithms"
    print "\n\tadd_constraint tests whether your add_constraint \n\tand dual simplex implementation can handle new constraints correctly\n\n"

elif sys.argv[1] == 'simplex':
    print "Simplex method: "
    for t in range(0,30):
        run_test_single(t, True, s.simplex)

elif sys.argv[1] == 'revised':
    print "Revised simplex method: "
    for t in range(0,30):
        run_test_single(t, True, s.revised_simplex)

elif sys.argv[1] == 'dual':
    print "Dual simplex method: "
    for t in range(0,30):
        run_test_single(t, False, s.dual_simplex)


elif sys.argv[1] == 'revised':
    for t in range(0,30):
        run_test_single(t, False, s.dual_simplex)

elif sys.argv[1] == 'compare_time':
    for t in range(20,30):
        run_test_compare2(t)

elif sys.argv[1] == 'add_constraint':
    for t in range(30,40):
        add_constraint_test(t)

