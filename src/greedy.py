from __future__ import annotations
import heapq
from typing import Dict, List, Tuple
from data_structures import Graph


def dijkstra(graph: Graph, origin: int):
    """
    Implementa o algoritmo de Dijkstra para encontrar os caminhos mais curtos.
    
    Args:
        graph: Grafo com vértices e arestas ponderadas
        origin: ID do vértice de origem
        
    Returns:
        Tupla com:
        - dict: Distâncias mínimas do origin para cada vértice
        - dict: Predecessores para reconstruir caminhos
        - int: Número de arestas relaxadas (operações)
    """
    # Inicializa distâncias com infinito e origem com 0
    dist = {v: float('inf') for v in graph.vertices}
    prev = {v: None for v in graph.vertices}
    dist[origin] = 0.0
    
    # Fila de prioridade: (distância, vértice)
    heap = [(0.0, origin)]
    operations = 0

    while heap:
        cost, u = heapq.heappop(heap)
        
        # Pula se já foi processado com distância menor
        if cost != dist[u]:
            continue

        # Relaxa todas as arestas do vértice u
        for v, w in graph.neighbors(u):
            operations += 1
            new_dist = cost + w
            
            # Se encontrou caminho mais curto, atualiza
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev, operations


def reconstruct_path(prev, origin, dest):
    """
    Reconstrói o caminho do destino até a origem usando predecessores.
    
    Args:
        prev: Dicionário de predecessores (de Dijkstra)
        origin: ID do vértice de origem
        dest: ID do vértice de destino
        
    Returns:
        Lista representando o caminho de origin até dest (vazio se não existe)
    """
    path = []
    current = dest

    while current is not None:
        path.append(current)
        if current == origin:
            break
        current = prev[current]

    # Retorna o caminho invertido se é válido (chegou na origem)
    return list(reversed(path)) if path and path[-1] == origin else []


def prim_mst(graph: Graph, start: int):
    """
    Implementa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST).
    
    Args:
        graph: Grafo com vértices e arestas ponderadas
        start: ID do vértice inicial
        
    Returns:
        Dict com:
        - 'mst': Lista de arestas da MST
        - 'cost': Custo total da MST
        - 'operations': Número de operações executadas
    """
    visited = {start}  # Vértices já inclusos na MST
    heap = []  # Fila de prioridade: (peso, origem, destino)
    mst = []  # Arestas selecionadas para a MST
    total_cost = 0.0
    operations = 0

    # Adiciona todas as arestas do vértice inicial
    for v, w in graph.neighbors(start):
        heapq.heappush(heap, (w, start, v))

    # Processa vértices até incluir todos
    while heap and len(visited) < len(graph.vertices):
        w, u, v = heapq.heappop(heap)
        operations += 1

        # Pula se vértice já foi visitado
        if v in visited:
            continue

        # Inclui vértice e aresta na MST
        visited.add(v)
        mst.append((u, v, w))
        total_cost += w

        # Adiciona arestas do novo vértice para vértices não visitados
        for next_v, next_w in graph.neighbors(v):
            if next_v not in visited:
                heapq.heappush(heap, (next_w, v, next_v))

    return {
        'mst': mst,
        'cost': total_cost,
        'operations': operations
    }


def kruskal_mst(graph: Graph):
    """
    Implementa o algoritmo de Kruskal para encontrar a Árvore Geradora Mínima.
    
    Args:
        graph: Grafo com vértices e arestas ponderadas
        
    Returns:
        Dict com:
        - 'mst': Lista de arestas da MST
        - 'cost': Custo total da MST
        - 'operations': Número de operações executadas
    """
    # Inicializa estrutura de dados Union-Find
    parent = {v: v for v in graph.vertices}
    rank = {v: 0 for v in graph.vertices}

    def find(x):
        """Encontra o representante do conjunto contendo x (com compressão de caminho)."""
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        """Une dois conjuntos. Retorna True se foram unidos, False se já estavam."""
        ra, rb = find(a), find(b)
        if ra == rb:
            return False

        # Une por rank (mantém árvore mais balanceada)
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1

        return True

    mst = []
    total_cost = 0.0
    operations = 0

    # Ordena arestas por peso (estratégia gulosa)
    for u, v, w in sorted(graph.edges(), key=lambda e: e[2]):
        operations += 1

        # Adiciona aresta se conecta componentes diferentes (sem ciclo)
        if union(u, v):
            mst.append((u, v, w))
            total_cost += w

    return {
        'mst': mst,
        'cost': total_cost,
        'operations': operations
    }
