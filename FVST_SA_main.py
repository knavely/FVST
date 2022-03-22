from gurobipy import *
from networkx import *

# Given a tournament T, we construct two LP relaxations for the feedback vertex set problem in T.
# We then compare these relaxations on tournaments of up to 7 vertices.

def P(T, solve = 1): # Construct basic relaxation P(T)

    m = Model()
    x = m.addVars(T.nodes(), ub=1, name='x')

    for [i,j,k] in dir_triangles(T.copy()):
        m.addConstr(x[i]+x[j]+x[k] >= 1)

    m.setObjective(x.sum(), GRB.MINIMIZE)
    if solve:
        m.optimize()
        # print('Solution: ' + str([x[v].X for v in T.nodes()]))

    return m

def SA_1(T, solve =1): # Construct Sherali-Adams relaxation SA_1(T).

    m = Model()
    x = m.addVars(T.nodes(), ub=1, name='x')

    pairs = [(min(i,j),max(i,j)) for (i,j) in T.edges()]
    y = m.addVars(pairs, lb = 0, name = 'y')

    for (i,j) in pairs:
        m.addConstr(y[i, j] <= x[i])
        m.addConstr(y[i, j] <= x[j])
        m.addConstr(y[i, j] >= x[i] + x[j]-1)

    for tri in dir_triangles(T.copy()):
        tri.sort()
        [i,j,k]= tri

        m.addConstr(x[i] + x[j] + x[k] >= 1 + y[i, j] + y[j, k])
        m.addConstr(x[i] + x[j] + x[k] >= 1 + y[i, k] + y[j, k])
        m.addConstr(x[i] + x[j] + x[k] >= 1 + y[i, j] + y[i, k])
        for d in T.nodes():
            if d not in [i,j,k]:
                m.addConstr(y[min(i,d),max(i,d)] + y[min(j,d),max(j,d)] + y[min(k,d),max(k,d)] >= x[d])
                m.addConstr(x[i] + x[j] + x[k] + x[d] >= 1+ y[min(i, d), max(i, d)] + y[min(j, d), max(j, d)] + y[min(k, d), max(k, d)])

    m.setObjective(x.sum(), GRB.MINIMIZE)
    if solve:
        m.optimize()
        # print('Solution: ' + str([x[v].X for v in T.nodes()]))
        # print('Y: ' + str([y[i,j].X for (i,j) in pairs]))

    return m



def dir_triangles(T): #lists all the directed triangles of T
    triangles = []
    nodes = [v for v in T]
    for i in nodes:
        for j in T.successors(i):
            for k in T.predecessors(i):
                if T.has_edge(j,k):
                    triangles.append([i,j,k])
        T.remove_node(i)

    return triangles

# We now test the two relaxations on some tournaments
# Tournaments from T_5:
T = DiGraph()
T.add_nodes_from(['a','b','c','d','e'])
T.add_edges_from([('a','b'),('c','a'),('a','d'),('e','a'),('c','b'),('b','d'),('b','e'), ('d','c'),('e','c'), ('d','e')])

P(T.copy())
SA_1(T.copy())

T = DiGraph()
T.add_nodes_from(['a','b','c','d','e'])
T.add_edges_from([('b','a'),('c','a'),('a','d'),('e','a'),('c','b'),('b','d'),('b','e'), ('d','c'),('e','c'), ('d','e')])

P(T.copy())
SA_1(T.copy())


T = DiGraph()
T.add_nodes_from(['a','b','c','d','e'])
T.add_edges_from([('a','b'),('c','a'),('d','a'),('e','a'),('b','c'),('b','d'),('b','e'), ('c','d'),('e','c'), ('d','e')])

P(T.copy())
SA_1(T.copy())


# light T_7
T = DiGraph()
T.add_nodes_from(['a','b','c','d','e','f','g'])
T.add_edges_from([('b','a'),('c','a'),('a','d'),('e','a'),('c','b'),('b','d'),('b','e'), ('d','c'),('e','c'), ('d','e'),
                  ('f','g'), ('f','a'),('f','b'), ('g','c'),('g','d'),('g','e'),('d','f'),('c','f'),('e','f'),('g','a'),
                  ('g','b')])

P(T.copy())
SA_1(T.copy())
