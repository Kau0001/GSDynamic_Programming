from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from collections import deque

# Type aliases para clareza
Vertex = Tuple[int, str, float, float, int, float, float]  # (id, nome, risco, pop, area, lat, lon)
Edge = Tuple[int, int, float]  # (origem, destino, peso)

class Graph:
    """Representa um grafo com vértices e arestas ponderadas."""
    
    def __init__(self, directed: bool = False):
        """
        Inicializa um grafo vazio.
        
        Args:
            directed: Se True, o grafo é direcionado; se False, não-direcionado.
        """
        self.directed = directed
        self.vertices: Dict[int, Vertex] = {}  # Armazena vértices por ID
        self.adj: Dict[int, List[Tuple[int, float]]] = {}  # Lista de adjacência: id -> [(vizinho, peso)]

    def add_vertex(self, vertex: Vertex) -> None:
        """Adiciona um vértice ao grafo."""
        vid = vertex[0]
        self.vertices[vid] = vertex
        self.adj.setdefault(vid, [])

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """
        Adiciona uma aresta entre dois vértices com peso.
        
        Args:
            u: ID do vértice de origem
            v: ID do vértice de destino
            weight: Peso da aresta
            
        Raises:
            ValueError: Se algum vértice não existe no grafo
        """
        if u not in self.vertices or v not in self.vertices:
            raise ValueError('Vértices precisam existir antes de adicionar aresta.')
        
        self.adj.setdefault(u, []).append((v, weight))
        # Se não-direcionado, adiciona a aresta inversa
        if not self.directed:
            self.adj.setdefault(v, []).append((u, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        """Retorna lista de vizinhos e pesos das arestas do vértice u."""
        return self.adj.get(u, [])

    def edges(self) -> List[Edge]:
        """Retorna lista de todas as arestas do grafo (sem duplicatas)."""
        seen = set()
        result = []
        
        for u, neighbors_list in self.adj.items():
            for v, w in neighbors_list:
                # Para grafos não-direcionados, usa chave ordenada para evitar duplicatas
                key = tuple(sorted((u, v))) if not self.directed else (u, v)
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        
        return result

    def bfs(self, start: int) -> List[int]:
        """
        Busca em largura (BFS) a partir de um vértice inicial.
        
        Returns:
            Lista de vértices visitados em ordem de descoberta
        """
        visited = {start}
        queue = deque([start])
        order = []
        
        while queue:
            u = queue.popleft()
            order.append(u)
            
            for v, _ in self.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return order



@dataclass
class Node:
    """Nó de uma Árvore Binária de Busca."""
    key: float  # Chave para ordenação (índice de risco)
    vertex: Vertex  # Dados do vértice armazenados
    left: Optional['Node'] = None  # Subárvore esquerda
    right: Optional['Node'] = None  # Subárvore direita


class BinarySearchTree:
    """Árvore Binária de Busca para buscar vértices por intervalo de risco."""
    
    def __init__(self):
        """Inicializa uma BST vazia."""
        self.root: Optional[Node] = None

    def insert(self, vertex: Vertex) -> None:
        """
        Insere um vértice na árvore usando seu índice de risco como chave.
        
        Args:
            vertex: Vértice a ser inserido (chave = vertex[2])
        """
        def _insert(node: Optional[Node], vertex: Vertex) -> Node:
            if node is None:
                return Node(vertex[2], vertex)
            
            # Insere à esquerda se o risco é menor, à direita caso contrário
            if vertex[2] < node.key:
                node.left = _insert(node.left, vertex)
            else:
                node.right = _insert(node.right, vertex)
            
            return node
        
        self.root = _insert(self.root, vertex)

    def search_range(self, r_min: float, r_max: float) -> List[Vertex]:
        """
        Busca todos os vértices com risco no intervalo [r_min, r_max].
        
        Returns:
            Lista de vértices dentro do intervalo
        """
        result = []
        
        def _walk(node: Optional[Node]):
            if not node:
                return
            
            # Caminha pela subárvore esquerda se chave pode estar lá
            if node.key >= r_min:
                _walk(node.left)
            
            # Adiciona o nó atual se está no intervalo
            if r_min <= node.key <= r_max:
                result.append(node.vertex)
            
            # Caminha pela subárvore direita se chave pode estar lá
            if node.key <= r_max:
                _walk(node.right)
        
        _walk(self.root)
        return result

    def inorder(self) -> List[Vertex]:
        """
        Retorna lista de todos os vértices em ordem crescente de risco.
        
        Returns:
            Lista de vértices ordenados por índice de risco
        """
        result = []
        
        def _walk(node):
            if node:
                _walk(node.left)
                result.append(node.vertex)
                _walk(node.right)
        
        _walk(self.root)
        return result

    def height(self) -> int:
        """Calcula a altura da árvore."""
        def _calculate_height(node):
            if node is None:
                return 0
            left_height = _calculate_height(node.left)
            right_height = _calculate_height(node.right)
            return 1 + max(left_height, right_height)
        
        return _calculate_height(self.root)

    def remove(self, vertex_id: int) -> None:
        """
        Remove um vértice da árvore usando reconstrução.
        
        Args:
            vertex_id: ID do vértice a ser removido
        """
        # Obtém todos os vértices exceto o que será removido
        ordered = [v for v in self.inorder() if v[0] != vertex_id]
        
        # Reconstrói a árvore
        self.root = None
        for v in ordered:
            self.insert(v)


def build_graph(vertices: List[Vertex], edges: List[Edge], directed: bool = False) -> Graph:
    """
    Constrói um grafo a partir de listas de vértices e arestas.
    
    Args:
        vertices: Lista de vértices
        edges: Lista de arestas
        directed: Se True, cria um grafo direcionado
        
    Returns:
        Grafo construído
    """
    g = Graph(directed)
    
    # Adiciona todos os vértices
    for v in vertices:
        g.add_vertex(tuple(v))
    
    # Adiciona todas as arestas
    for u, v, w in edges:
        g.add_edge(u, v, float(w))
    
    return g


def build_bst(vertices: List[Vertex]) -> BinarySearchTree:
    """
    Constrói uma Árvore Binária de Busca a partir de uma lista de vértices.
    
    Args:
        vertices: Lista de vértices para inserir na árvore
        
    Returns:
        BST construída
    """
    bst = BinarySearchTree()
    for v in vertices:
        bst.insert(tuple(v))
    return bst
