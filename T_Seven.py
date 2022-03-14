from sage.all import *
import itertools

#We use sage and naughty to work will all tournaments of size 7 given
#these are given in matrix format (A), but we convert to lists of triangles (trips).

def to_digraph_trips(A,n = 7):
    trips = [(a,b,c) for (a,b,c) in itertools.combinations(range(n),3)
          if ((A[a,b] == 1 and A[b,c] == 1 and A[c,a] == 1) or
              (A[a,c] == 1 and A[c,b] == 1 and A[b,a] == 1) or
              (A[b,a] == 1 and A[a,c] == 1 and A[c,a] == 1) or
              (A[b,c] == 1 and A[c,a] == 1 and A[a,b] == 1) or
              (A[c,a] == 1 and A[a,b] == 1 and A[b,c] == 1) or
              (A[c,b] == 1 and A[b,a] == 1 and A[a,c] == 1))
          ]
    return trips

#a set of vertices si is feasible for FVST if it intersects each triangle
def is_feasible(trips,si):
    for t in trips:
        if si.intersection(t) == set():
            return False
    return True

#pair (a,b) is diagonal with respect to a set of triples X and Y
#if a in X, b in Y and \X U Y\ = 4
def is_diag(pair, trips):
    (a, b) = pair
         return [
             set(x + y)
             for x in trips
             for y in trips
             if a in x and b not in x and b in y and a not in y and len(set(x + y)) == 4
         ]

#a list of triples is heavy if it has two diagonals.
#first find all diagonals testing each pair in [7] using is_diag
#then for each triple, check if it contains two diagonals
def is_heavy(trips,n = 7):
    diag = [set(p) for p in itertools.combinations(range(n),2) if is_diag(p,trips)]
    #print diag
    two = [(a,b,c) for (a,b,c) in trips if (
        ({a,b} in diag and {a,c} in diag) or ({a,b} in diag and {b,c} in diag)
        or {a,c} in diag and {b,c} in diag)]
    return two

#A tournament on 7 vertices is a T_7 if it does not contain a feasible solution of size 2
def is_T7(trips,n = 7):
    twoFeasible = [s for s in itertools.combinations(range(n),2) if is_feasible(trips,set(s))]
    return not twoFeasible

#we can obtain all T7s checking each tournament on 7 vertices using is_T7
def all_T7():
    tg = digraphs.tournaments_nauty(7)
    t7 = []
    for g in tg:
        tr = to_digraph_trips(g.adjacency_matrix(),7)
        if is_T7(tr):
            t7.append(tr)
    return t7

#now we can get all T_7s
t_sevens = all_T7()

#|T_7| = 121
len(t_sevens)

#find all T_7 that are not heavy
lightT7s = [t for t in ti if not has2(t, 7)]

# light T_7 which we discovered
snark = [(0, 2, 5),(0, 3, 5),(0, 4, 5), (1, 2, 4),(1, 2, 5),(1, 3, 4),(1, 3, 5),(2, 3, 6),(2, 4, 6),(2, 5, 6)]

#there is exactly one light T_7
lightT7 == [snark]

