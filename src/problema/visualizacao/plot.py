import matplotlib.pyplot as plt

def plotar_mapa(largura, altura, obstaculos, grafo=None, caminho=None):
    """
    Plota os obstáculos (triângulos), o ponto de inicio e o objetivo no mapa.
    
    Args:
        largura: Largura do mapa
        altura: Altura do mapa
        obstaculos: Lista de objetos Triangulo
        grafo: Dicionário {triangulo: lista de vizinhos} para plotar arestas do grafo
        caminho: Lista de triangulos no caminho encontrado
        ponto de inicio: Inicio do mapa
        objetivo: Ponto final do mapa
    """
    fig, ax = plt.subplots(figsize=(10,10))

    # Margem de 5% para melhor visualização
    margem_x = largura * 0.05 if largura > 0 else 1
    margem_y = altura * 0.05 if altura > 0 else 1
    ax.set_xlim(-margem_x, largura + margem_x)
    ax.set_ylim(-margem_y, altura + margem_y)
    ax.set_aspect('equal')
    
    # Plotar obstáculos
    for triangulo in obstaculos:
        # Extrair vértices do dicionário de adjacências
        vertices = list(triangulo.adj.keys())
        
        if len(vertices) >= 3:
            # Ordena os vértices para formar um polígono válido
            # Para um triângulo equilátero, ordena por ângulo
            centro = (sum(v[0] for v in vertices) / len(vertices), 
                     sum(v[1] for v in vertices) / len(vertices))
            
            vertices_sorted = sorted(vertices, 
                                    key=lambda v: __import__('math').atan2(v[1] - centro[1], 
                                                                             v[0] - centro[0]))
            
            # Fecha o polígono repetindo o primeiro vértice
            vertices_sorted.append(vertices_sorted[0])
            xs, ys = zip(*vertices_sorted)
            ax.fill(xs, ys, "blue", edgecolor="black", linewidth=0.5)
    
    # Plotar vértices
    if grafo:
        all_vertices = list(grafo.keys())
        ax.scatter([v[0] for v in all_vertices], [v[1] for v in all_vertices], c='black', s=10, zorder=5)
    
    # Plotar arestas do grafo se fornecido
    if grafo:
        for v1, vizinhos in grafo.items():
            for v2 in vizinhos:
                if v1 < v2:  # Evitar plotar duas vezes
                    ax.plot([v1[0], v2[0]], [v1[1], v2[1]], 'k-', alpha=0.3)
    
    
    # Plot do inicio e do objetivo
    ax.plot(0, 0, marker='o', color='green', markersize=12, label='Início (0,0)')
    ax.plot(largura, altura, marker='x', color='red', markersize=12, label=f'Objetivo ({largura}, {altura})')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.title(f"Mapa com {len(obstaculos)} Obstáculos")
    plt.grid(True, alpha=0.3)
    
    # Legenda para diferenciar
    plt.legend()

    # Salvar figura em arquivo
    output_path = "mapa_obstaculos.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Mapa salvo em: {output_path}")
    plt.close()
