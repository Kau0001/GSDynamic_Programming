from __future__ import annotations
from typing import Dict, List, Tuple, Any
from itertools import combinations
from data_structures import Graph


class BruteForceResult:
    """Armazena resultados do algoritmo de força bruta."""
    
    def __init__(self, best_path, best_cost, paths_evaluated, recursive_calls):
        """
        Args:
            best_path: Melhor caminho encontrado
            best_cost: Custo do melhor caminho
            paths_evaluated: Número de caminhos completos avaliados
            recursive_calls: Número total de chamadas recursivas
        """
        self.best_path = best_path
        self.best_cost = best_cost
        self.paths_evaluated = paths_evaluated
        self.recursive_calls = recursive_calls


def all_paths_shortest(graph: Graph, origin: int, dest: int) -> BruteForceResult:
    """
    Encontra o caminho mais curto usando busca exaustiva (força bruta).
    Explora todos os caminhos possíveis do origin ao dest.
    
    Args:
        graph: Grafo com vértices e arestas ponderadas
        origin: ID do vértice de origem
        dest: ID do vértice de destino
        
    Returns:
        BruteForceResult com o melhor caminho e estatísticas
    """
    best_path = None
    best_cost = float('inf')
    recursive_calls = 0
    paths_evaluated = 0

    def dfs(u, target, visited, path, cost):
        """
        Busca em profundidade (DFS) explorando todos os caminhos.
        
        Args:
            u: Vértice atual
            target: Vértice de destino
            visited: Conjunto de vértices já visitados neste caminho
            path: Caminho atual do origin até u
            cost: Custo acumulado do caminho
        """
        nonlocal best_path, best_cost, recursive_calls, paths_evaluated
        
        recursive_calls += 1

        # Se chegou no destino, avalia o caminho
        if u == target:
            paths_evaluated += 1
            if cost < best_cost:
                best_cost = cost
                best_path = path[:]  # Cópia do caminho
            return

        # Explora todos os vizinhos não visitados
        for v, w in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                path.append(v)
                
                # Recursão: continua caminhando
                dfs(v, target, visited, path, cost + w)
                
                # Backtracking: desfaz a escolha
                path.pop()
                visited.remove(v)

    # Inicia a DFS do origin
    dfs(origin, dest, {origin}, [origin], 0.0)

    return BruteForceResult(best_path, best_cost, paths_evaluated, recursive_calls)


def brute_force_mst(graph: Graph):
    """
    Encontra a Árvore Geradora Mínima usando busca exaustiva.
    Testa todas as combinações de arestas e verifica se formam uma MST válida.
    
    Args:
        graph: Grafo com vértices e arestas ponderadas
        
    Returns:
        Dict com:
        - 'mst': Lista de arestas da MST encontrada
        - 'cost': Custo total da MST
        - 'subtrees_evaluated': Número de combinações de arestas testadas
    """
    vertices = list(graph.vertices.keys())
    n = len(vertices)
    edge_list = graph.edges()
    
    best_mst = None
    best_cost = float('inf')
    subtrees_evaluated = 0
    parent = {}  # Para verificar conectividade

    def connected_and_acyclic(edges):
        """
        Verifica se um conjunto de arestas forma uma árvore válida.
        Usa Union-Find para detectar ciclos e verificar conectividade.
        
        Args:
            edges: Lista de arestas a testar
            
        Returns:
            True se forma uma árvore acíclica e conectada
        """
        parent.clear()

        def find(x):
            """Encontra representante com compressão de caminho."""
            parent.setdefault(x, x)
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(a, b):
            """Une dois conjuntos. Retorna False se cria ciclo."""
            ra, rb = find(a), find(b)
            if ra == rb:
                return False  # Ciclo detectado
            parent[rb] = ra
            return True

        # Tenta unir todos os vértices
        for u, v, _ in edges:
            if not union(u, v):
                return False  # Ciclo encontrado

        # Verifica se todos os vértices estão conectados (componente única)
        return len({find(v) for v in vertices}) == 1

    # Testa todas as combinações de (n-1) arestas
    for combo in combinations(edge_list, n - 1):
        subtrees_evaluated += 1

        # Verifica se a combinação forma uma árvore válida
        if connected_and_acyclic(combo):
            cost = sum(w for _, _, w in combo)
            
            # Se é melhor que a anterior, atualiza
            if cost < best_cost:
                best_cost = cost
                best_mst = list(combo)

    return {
        'mst': best_mst,
        'cost': best_cost,
        'subtrees_evaluated': subtrees_evaluated
    }
