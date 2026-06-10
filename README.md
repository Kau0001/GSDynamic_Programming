# Global Solution Dynamic_Programming - Monitoramento Ambiental Inteligente

## Integrantes do Grupo

| Nome | RM |
|--------|--------|
| Kauã Gabriel Moreira e Silva | RM566043 |
| Ana Clara Rocha de Oliveira | RM564298 |
| Kaike Correia da Silva | RM561623 |
| Vitor Alcantara | RM565885 |
| Vitor Fernandes dos Santos | RM566275 |

---

# Descrição do Projeto

O projeto tem como objetivo desenvolver uma solução computacional para análise e monitoramento ambiental utilizando estruturas de dados e algoritmos estudados na disciplina.

A aplicação processa informações ambientais como índices de vegetação (NDVI), dados pluviométricos e malha viária, permitindo a modelagem de cenários e análise de conectividade por meio de grafos.

O sistema utiliza diferentes abordagens algorítmicas para comparação de desempenho e eficiência na resolução dos problemas propostos.

---

# Objetivos

- Aplicar estruturas de dados na resolução de problemas reais.
- Implementar algoritmos de grafos para análise ambiental.
- Comparar soluções por força bruta e algoritmos gulosos.
- Desenvolver uma arquitetura organizada e escalável.
- Gerar resultados que auxiliem na tomada de decisão ambiental.

---

# Tecnologias Utilizadas

- Python 3.12
- JSON
- Git
- GitHub

---

# 📂 Estrutura do Projeto

```text
global-solution-2026-fund/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── ndvi.csv
│   │   ├── pluviometria.csv
│   │   └── malha_viaria.csv
│   │
│   └── processed/
│       ├── grafo.json
│       └── arvore.pkl
│
└── src/
    ├── data_structures.py
    ├── brute_force.py
    └── greedy.py
```

---

# 📚 Descrição dos Módulos

## data_structures.py

Responsável pela implementação das estruturas de dados utilizadas no projeto:

- Lista
- Tupla
- Dicionário
- Heap
- Árvore Binária
- Grafo

---

## brute_force.py

Implementação da estratégia de força bruta utilizada como método de validação dos resultados obtidos pelos algoritmos otimizados.

Características:

- Enumeração completa das possibilidades.
- Garantia da solução ótima.
- Alto custo computacional.

---

## greedy.py

Implementação dos algoritmos gulosos utilizados para otimização.

Algoritmos implementados:

### Prim

Utilizado para encontrar a Árvore Geradora Mínima (MST).

### Kruskal

Outra abordagem para obtenção da MST em grafos ponderados.

### Dijkstra

Utilizado para encontrar os menores caminhos entre vértices de um grafo.

---

# Como Executar

## 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/global-solution-2026-fund.git
```

## 2. Acessar a Pasta

```bash
cd global-solution-2026-fund
```

## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 4. Executar o Projeto

### Força Bruta

```bash
python src/brute_force.py
```

### Algoritmos Gulosos

```bash
python src/greedy.py
```

---

# Dados Utilizados

Os dados processados pelo sistema incluem:

- Índice de Vegetação (NDVI)
- Dados de Pluviometria
- Malha Viária
- Redes de Conectividade

Os arquivos brutos são armazenados na pasta:

```text
data/raw/
```

Os arquivos processados são armazenados em:

```text
data/processed/
```

---

# Resultados Esperados

- Construção de grafos ambientais.
- Análise de conectividade entre regiões.
- Comparação entre algoritmos.
- Identificação de caminhos mínimos.
- Geração de estruturas otimizadas para suporte à tomada de decisão.

---

# Controle de Versão

O projeto utiliza Git e GitHub para controle de versão.

Todos os integrantes do grupo participam do desenvolvimento através de commits distribuídos no repositório, conforme solicitado nas diretrizes da Global Solution.

---

# Disciplina

Global Solution 2026

Fundamentos de Estruturas de Dados e Algoritmos

FIAP - Faculdade de Informática e Administração Paulista

---

## Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais.
