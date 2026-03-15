import matplotlib.pyplot as plt

def plotar_mapa(largura, altura, obstaculos):
    """
    Plota os obstáculos (triângulos), o ponto de inicio e o objetivo no mapa.
    
    Args:
        largura: Largura do mapa
        altura: Altura do mapa
        obstaculos: Lista de objetos Triangulo
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
    
    # Plot do inicio e do objetivo
    ax.plot(0,altura, marker='o', color='green', markersize=12, label=f'Início (0,{altura})')
    ax.plot(largura, 0, marker='x', color='red', markersize=12, label=f'Objetivo ({largura}, 0)')

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
