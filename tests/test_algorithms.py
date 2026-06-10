import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]/'src'))
from data_structures import build_graph, build_bst
from brute_force import all_paths_shortest
from greedy import dijkstra, reconstruct_path, prim_mst, kruskal_mst

def sample():
    vertices=[(1,'A',0.5,100,1000,0,0),(2,'B',0.7,100,1000,0,1),(3,'C',0.9,100,1000,1,0),(4,'D',0.6,100,1000,1,1)]
    edges=[(1,2,1),(2,4,1),(1,3,5),(3,4,1),(2,3,2)]
    return build_graph(vertices,edges), vertices

def test_bst_range():
    _, vertices=sample(); bst=build_bst(vertices)
    names=[v[1] for v in bst.search_range(0.6,0.8)]
    assert set(names)=={'B','D'}

def test_dijkstra_equals_bruteforce():
    g,_=sample(); bf=all_paths_shortest(g,1,4); dist,prev,ops=dijkstra(g,1)
    assert dist[4] == bf.best_cost
    assert reconstruct_path(prev,1,4) == [1,2,4]

def test_mst_algorithms():
    g,_=sample(); p=prim_mst(g,1); k=kruskal_mst(g)
    assert p['cost'] == k['cost'] == 3
