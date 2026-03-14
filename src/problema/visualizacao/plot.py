import matplotlib.pyplot as plt

def plotar_mapa(largura, altura, obstaculos):
    """
    Plota os obstáculos (triângulos) no mapa.
    
    Args:
        largura: Largura do mapa
        altura: Altura do mapa
        obstaculos: Lista de objetos Triangulo
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
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
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.title(f"Mapa com {len(obstaculos)} Obstáculos")
    plt.grid(True, alpha=0.3)
    
    # Salvar figura em arquivo
    output_path = "mapa_obstaculos.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Mapa salvo em: {output_path}")
    plt.close()
