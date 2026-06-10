from __future__ import annotations
import random
import time
import tracemalloc
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from data_structures import Graph, build_graph, build_bst
from brute_force import all_paths_shortest
from greedy import dijkstra, reconstruct_path, prim_mst
from visualizar import plot_performance, plot_gap


def synthetic_graph(n: int, seed: int = 42) -> Graph:
    """
    Gera um grafo sintético com n vértices para benchmark.
    Simula municípios brasileiros com coordenadas geográficas.
    
    Args:
        n: Número de vértices
        seed: Seed do gerador aleatório
        
    Returns:
        Grafo com vértices aleatórios e arestas parcialmente conectadas
    """
    random.seed(seed + n)

    # Cria vértices: (id, nome, risco, população, área, latitude, longitude)
    vertices = []
    for i in range(n):
        vertices.append((
            1000 + i,
            f'Municipio{i}',
            random.random(),  # Risco (0-1)
            random.randint(800, 2000),  # População (mil)
            random.randint(10000, 200000),  # Área (km²)
            -30 + random.random() * 5,  # Latitude
            -55 + random.random() * 5  # Longitude
        ))

    # Cria arestas: começa com linha linear, depois adiciona conexões aleatórias
    edges = []

    # Conecta vértices consecutivos (garante conectividade)
    for i in range(n - 1):
        edges.append((
            1000 + i,
            1000 + i + 1,
            round(random.uniform(0.5, 4.0), 2)
        ))

    # Adiciona arestas aleatórias adicionais
    for i in range(n):
        for j in range(i + 2, n):
            # Probabilidade diminui com tamanho do grafo
            if random.random() < min(0.25, 5 / n):
                edges.append((
                    1000 + i,
                    1000 + j,
                    round(random.uniform(0.5, 5.0), 2)
                ))

    return build_graph(vertices, edges)


def measure(fn):
    """
    Mede tempo de execução e memória usada por uma função.
    
    Args:
        fn: Função a executar
        
    Returns:
        Tupla: (resultado, tempo_ms, pico_memória_mb)
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Executa função
    result = fn()
    
    # Coleta métricas
    elapsed = (time.perf_counter() - start_time) * 1000  # Converte para ms
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, elapsed, peak_mem / (1024 * 1024)  # Converte pico para MB


def benchmark():
    """
    Executa benchmark comparando:
    - Força bruta (até n=12)
    - Dijkstra (guloso)
    
    Calcula gap de otimalidade (diferença % do guloso para o ótimo).
    Salva resultados em JSON e gera gráficos.
    
    Returns:
        Lista de resultados dos benchmarks
    """
    results = []

    # Testa com diferentes tamanhos de grafo
    for n in [5, 8, 10, 12, 20, 50, 100]:
        print(f'Testando com n={n}...')
        
        g = synthetic_graph(n)
        origin = 1000
        dest = 1000 + n - 1

        # Força bruta: só faz para grafos pequenos (computacionalmente intensivo)
        if n <= 12:
            bf_result, brute_force_ms, brute_force_mem = measure(
                lambda: all_paths_shortest(g, origin, dest)
            )
            optimal_cost = bf_result.best_cost
        else:
            brute_force_ms = None
            brute_force_mem = None
            optimal_cost = None

        # Dijkstra: algoritmo guloso (rápido, mas não garante ótimo)
        dijkstra_result, dijkstra_ms, dijkstra_mem = measure(
            lambda: dijkstra(g, origin)
        )
        dist, prev, ops = dijkstra_result
        greedy_cost = dist[dest]

        # Calcula gap: (greedy - optimal) / optimal * 100
        gap = 0.0 if optimal_cost in (None, 0) else max(0, (greedy_cost - optimal_cost) / optimal_cost * 100)

        # Armazena resultado
        results.append({
            'N': n,
            'brute_force_ms': brute_force_ms,
            'brute_force_mem_mb': brute_force_mem,
            'greedy_ms': dijkstra_ms,
            'greedy_mem_mb': dijkstra_mem,
            'greedy_cost': greedy_cost,
            'optimal_cost': optimal_cost,
            'gap_percent': gap,
            'operations_greedy': ops
        })

    # Salva resultados em JSON
    output_file = Path(__file__).resolve().parents[1] / 'data/processed/performance_results.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(results, indent=2), encoding='utf-8')

    # Gera gráficos
    figure_dir = Path(__file__).resolve().parents[1] / 'report/figures'
    
    # Gráfico de performance (preenche None com 0 para plotagem)
    results_with_zeros = [
        dict(r, brute_force_ms=(r['brute_force_ms'] or 0))
        for r in results
    ]
    plot_performance(results_with_zeros, figure_dir / 'performance.png')
    plot_gap(results, figure_dir / 'gap.png')

    return results


if __name__ == '__main__':
    print('Iniciando benchmark de algoritmos...\n')
    benchmark_results = benchmark()
    
    print('\n--- Resultados do Benchmark ---')
    for r in benchmark_results:
        print(r)
