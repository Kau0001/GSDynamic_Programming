# Global Solution 2026 - Monitoramento de Riscos Ambientais

Projeto em Python para a FIAP: modelagem de municípios como grafo ponderado, organização de risco em BST, comparação entre Força Bruta e algoritmo Guloso.

## Integrantes
Kauã Gabriel Moreira e Silva - rm566043
Ana Clara Rocha de Oliveira - rm564298 
Kaike Correia da Silva - rm561623
Vitor Alcantara - rm565885
Vitor Fernandes dos Santos - rm566275


## Cenários usados
1. Rede de resposta a enchentes no Rio Grande do Sul.
2. Triagem de risco de seca no MATOPIBA.

Os dados deste repositório são sintéticos, porém inspirados nos cenários brasileiros propostos. Para a entrega final, é possível substituir os arquivos em `data/raw/` por dados reais de DNIT, Defesa Civil RS, INMET, IBGE, INPE ou NASA.

## Como executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
python src/performance_monitor.py
pytest
```

## Estrutura
- `src/data_structures.py`: grafo, BST, lista de adjacência e estruturas auxiliares.
- `src/brute_force.py`: enumeração exaustiva para instâncias pequenas.
- `src/greedy.py`: Dijkstra, Prim e Kruskal.
- `src/performance_monitor.py`: tempo, memória, operações e gráficos.
- `src/visualizations.py`: figuras obrigatórias do relatório.
- `tests/test_algorithms.py`: testes automatizados.
- `report/relatorio_final.pdf`: relatório técnico pronto para revisão.

## Decisão de algoritmo
O projeto usa Dijkstra como variante principal do Guloso para rotas de atendimento e Prim/Kruskal como apoio para MST. A Força Bruta valida instâncias pequenas e demonstra explosão combinatória.


