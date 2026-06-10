from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).parent))

from data_structures import build_graph, build_bst
from brute_force import all_paths_shortest
from greedy import dijkstra, reconstruct_path, prim_mst, kruskal_mst
from visualizar import plot_graph_mst, plot_bst


def load_rs():
    """
    Carrega dados de municípios do Rio Grande do Sul.
    
    Returns:
        Tupla: (lista_vertices, lista_arestas)
    """
    data_path = Path(__file__).resolve().parents[1] / 'data/raw/sample_brazilian_scenarios.json'
    data = json.loads(data_path.read_text(encoding='utf-8'))
    return data['rs_municipios'], data['rs_edges']


if __name__ == '__main__':
    print('=== Análise de Grafo: Municípios do Rio Grande do Sul ===\n')

    # Carrega dados
    print('Carregando dados...')
    vertices, edges = load_rs()
    
    # Constrói estruturas de dados
    print('Construindo grafo e BST...')
    g = build_graph(vertices, edges)
    bst = build_bst(vertices)

    # --- Busca por intervalo de risco ---
    print('\n--- Municípios de Alto Risco (risco: 70-100%) ---')
    high_risk = bst.search_range(0.70, 1.0)
    print(f'Encontrados {len(high_risk)} municípios:')
    for v in high_risk[:5]:  # Mostra primeiros 5
        print(f'  {v[1]}: risco={v[2]:.2%}')
    if len(high_risk) > 5:
        print(f'  ... e mais {len(high_risk) - 5} municípios')

    # --- Problema do Caminho Mais Curto ---
    print('\n--- Caminho Mais Curto ---')
    origin = 4314902
    dest = 4314100

    # Força bruta
    brute_force_result = all_paths_shortest(g, origin, dest)
    print(f'Força Bruta:')
    print(f'  Caminho: {brute_force_result.best_path}')
    print(f'  Custo: {brute_force_result.best_cost:.2f}')
    print(f'  Caminhos avaliados: {brute_force_result.paths_evaluated}')
    print(f'  Chamadas recursivas: {brute_force_result.recursive_calls}')

    # Dijkstra (algoritmo guloso - mais rápido)
    dist, prev, operations = dijkstra(g, origin)
    dijkstra_path = reconstruct_path(prev, origin, dest)
    dijkstra_cost = dist[dest]
    print(f'\nDijkstra (Guloso):')
    print(f'  Caminho: {dijkstra_path}')
    print(f'  Custo: {dijkstra_cost:.2f}')
    print(f'  Arestas relaxadas: {operations}')

    # --- Árvore Geradora Mínima ---
    print('\n--- Árvore Geradora Mínima (MST) ---')
    mst_prim = prim_mst(g, origin)
    print(f'Prim MST:')
    print(f'  Custo total: {mst_prim["cost"]:.2f}')
    print(f'  Arestas: {len(mst_prim["mst"])}')
    print(f'  Operações: {mst_prim["operations"]}')

    mst_kruskal = kruskal_mst(g)
    print(f'\nKruskal MST:')
    print(f'  Custo total: {mst_kruskal["cost"]:.2f}')
    print(f'  Arestas: {len(mst_kruskal["mst"])}')
    print(f'  Operações: {mst_kruskal["operations"]}')

    # --- Visualizações ---
    print('\n--- Gerando visualizações ---')
    figure_dir = Path(__file__).resolve().parents[1] / 'report/figures'
    
    plot_graph_mst(g, mst_prim['mst'], figure_dir / 'graph_mst.png')
    print(f'Grafo com MST salvo em: {figure_dir / "graph_mst.png"}')
    
    plot_bst(bst, figure_dir / 'bst.png')
    print(f'BST salva em: {figure_dir / "bst.png"}')

    print('\n✓ Análise concluída com sucesso!')
