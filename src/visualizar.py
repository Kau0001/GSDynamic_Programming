from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:
    nx = None

from data_structures import Graph, BinarySearchTree, Node


def plot_graph_mst(graph: Graph, mst_edges, path: str):
    """
    Visualiza um grafo com as arestas da MST destacadas em vermelho.
    
    Args:
        graph: Grafo a visualizar
        mst_edges: Lista de arestas da Árvore Geradora Mínima
        path: Caminho do arquivo para salvar a figura
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Se networkx não está disponível, retorna silenciosamente
    if nx is None:
        return

    # Cria grafo NetworkX
    G = nx.Graph()
    for vid, v in graph.vertices.items():
        G.add_node(vid, label=v[1])  # Adiciona nó com label (nome município)
    
    for u, v, w in graph.edges():
        G.add_edge(u, v, weight=w)  # Adiciona arestas

    # Define posições usando coordenadas geográficas (latitude, longitude)
    pos = {vid: (vert[6], vert[5]) for vid, vert in graph.vertices.items()}

    # Cria labels com primeiros nomes dos municípios
    labels = {vid: graph.vertices[vid][1].split()[0] for vid in graph.vertices}

    # Desenha grafo
    nx.draw(G, pos, with_labels=False, node_size=450)
    nx.draw_networkx_labels(G, pos, labels, font_size=7)
    
    # Destaca arestas da MST em vermelho e mais grossas
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v) for u, v, _ in mst_edges],
        width=3,
        edge_color='red'
    )

    plt.title('Grafo de municípios com MST destacada')
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_bst(bst: BinarySearchTree, path: str):
    """
    Visualiza uma Árvore Binária de Busca como diagrama.
    
    Args:
        bst: Árvore a visualizar
        path: Caminho do arquivo para salvar a figura
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')

    # Lista para armazenar coordenadas (nó, x, y)
    coords = []

    def assign_coordinates(node, depth=0, x=0, spread=1):
        """Atribui coordenadas aos nós para desenho em árvore."""
        if not node:
            return

        coords.append((node, x, -depth))

        # Recorre recursivamente para subárvores esquerda e direita
        assign_coordinates(node.left, depth + 1, x - spread, spread / 2)
        assign_coordinates(node.right, depth + 1, x + spread, spread / 2)

    assign_coordinates(bst.root, 0, 0, 4)

    # Desenha arestas (linhas entre nós pai e filhos)
    for node, x, y in coords:
        for child in [node.left, node.right]:
            if child:
                # Encontra coordenadas do filho
                cx, cy = next((xx, yy) for n, xx, yy in coords if n is child)
                ax.plot([x, cx], [y, cy], 'k-', linewidth=1)

    # Desenha nós com labels
    for node, x, y in coords:
        # Exibe nome do município e índice de risco
        label = f'{node.vertex[1][:8]}\n{node.key:.2f}'
        ax.text(
            x, y, label,
            ha='center', va='center',
            bbox=dict(boxstyle='round', fc='white', edgecolor='black')
        )

    ax.set_title('BST por índice de risco')
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_performance(results, path: str):
    """
    Plota gráfico de tempo de execução vs número de vértices.
    Compara Força Bruta com Algoritmo Guloso (Dijkstra).
    
    Args:
        results: Lista de dicts com resultados de benchmark
        path: Caminho do arquivo para salvar a figura
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Extrai dados para gráfico
    ns = [r['N'] for r in results]  # Número de vértices
    brute_force_times = [r['brute_force_ms'] for r in results]  # Tempos força bruta
    greedy_times = [r['greedy_ms'] for r in results]  # Tempos algoritmo guloso

    # Cria figura
    plt.figure(figsize=(7, 4))
    plt.plot(ns, brute_force_times, marker='o', label='Força Bruta')
    plt.plot(ns, greedy_times, marker='o', label='Guloso (Dijkstra)')
    plt.xlabel('N vértices')
    plt.ylabel('tempo (ms)')
    plt.title('Desempenho: Tempo de Execução x Número de Vértices')
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_gap(results, path: str):
    """
    Plota gráfico de gap de otimalidade vs número de vértices.
    Gap mede quanto o algoritmo guloso afasta da solução ótima.
    
    Args:
        results: Lista de dicts com resultados de benchmark
        path: Caminho do arquivo para salvar a figura
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    # Extrai dados
    ns = [r['N'] for r in results]  # Número de vértices
    gap_percentages = [r['gap_percent'] for r in results]  # Gaps em percentual

    # Cria figura
    plt.figure(figsize=(7, 4))
    plt.plot(ns, gap_percentages, marker='o', color='green')
    plt.xlabel('N vértices')
    plt.ylabel('gap (%)')
    plt.title('Gap de Otimalidade: Algoritmo Guloso vs Ótimo')
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
