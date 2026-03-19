import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

def plotar_mapa(largura, altura, obstaculos, grafo=None, inicio=None, fim=None, caminho=None):
    """
    Plota os obstáculos (triângulos), o ponto de inicio, objetivo e o grafo de visibilidade.
    
    Args:
        largura: Largura do mapa
        altura: Altura do mapa
        obstaculos: Lista de objetos Triangulo
        grafo: Dicionário do grafo de visibilidade {vert: [(viz, dist), ...]} (opcional)
        inicio: Ponto de início (opcional)
        fim: Ponto final (objetivo) (opcional)
        caminho: Lista de pontos (vértices) do caminho encontrado (opcional)
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Margem de 5% para melhor visualização
    margem_x = largura * 0.05 if largura > 0 else 1
    margem_y = altura * 0.05 if altura > 0 else 1
    ax.set_xlim(-margem_x, largura + margem_x)
    ax.set_ylim(-margem_y, altura + margem_y)
    ax.set_aspect('equal')
    
    # Plotar obstáculos
    for triangulo in obstaculos:
        vertices = list(triangulo.adj.keys())
        
        if len(vertices) >= 3:
            centro = (sum(v[0] for v in vertices) / len(vertices), 
                     sum(v[1] for v in vertices) / len(vertices))
            
            vertices_sorted = sorted(vertices, 
                                    key=lambda v: __import__('math').atan2(v[1] - centro[1], 
                                                                             v[0] - centro[0]))
            
            vertices_sorted.append(vertices_sorted[0])
            xs, ys = zip(*vertices_sorted)
            ax.fill(xs, ys, "blue", edgecolor="black", linewidth=0.5, alpha=0.6)
    
    # Plotar grafo de visibilidade se fornecido
    if grafo:
        edges_plotadas = set()
        for vert, vizinhos in grafo.items():
            for viz, dist in vizinhos:
                edge = tuple(sorted([vert, viz]))
                if edge not in edges_plotadas:
                    edges_plotadas.add(edge)
                    xs = [vert[0], viz[0]]
                    ys = [vert[1], viz[1]]
                    ax.plot(xs, ys, 'green', linewidth=0.5, alpha=0.4, linestyle='--')
        
        # Plotar vértices do grafo
        for vert in grafo.keys():
            ax.plot(vert[0], vert[1], 'ko', markersize=3, alpha=0.5)
    
    # Plot do inicio e do objetivo
    if inicio is None:
        inicio = (0.0, 0.0)
    if fim is None:
        fim = (largura, altura)
    
    ax.plot(inicio[0], inicio[1], marker='o', color='green', markersize=12, label=f'Início ({inicio[0]:.1f}, {inicio[1]:.1f})')
    ax.plot(fim[0], fim[1], marker='x', color='red', markersize=12, label=f'Objetivo ({fim[0]:.1f}, {fim[1]:.1f})')


    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.title(f"Mapa com {len(obstaculos)} Obstáculos")
    plt.tight_layout()
    plt.show()