from problema.triangulo.utils import Utils
from problema.triangulo.triangulo import Triangulo
from problema.visualizacao.plot import plotar_mapa

def pegar_linhas(triangulo):
    """Le o dicionário do grafo e devolve uma lista de linhas sem repetição."""
    lines = []
    visited = set()

    for point_a in triangulo.adj:
        for point_b in triangulo.adj[point_a]:
            line = tuple(sorted((point_a, point_b)))
            if line not in visited:
                visited.add(line)
                lines.append(line)
    return lines

def testar_colisao(triangulo1, triangulo2):
    """Wrapper para testar colisão entre dois triângulos."""
    return Utils.testar_colisao(triangulo1, triangulo2)


def ler_entrada_float(prompt):
    """Lê e valida entrada float do usuário."""
    while True:
        try:
            valor = float(input(prompt))
            if valor <= 0:
                print("❌ Valor deve ser positivo!")
                continue
            return valor
        except ValueError:
            print("❌ Digite um número válido!")


def ler_entrada_int(prompt):
    """Lê e valida entrada inteira do usuário."""
    while True:
        try:
            valor = int(input(prompt))
            if valor <= 0:
                print("❌ Valor deve ser positivo!")
                continue
            return valor
        except ValueError:
            print("❌ Digite um número inteiro válido!")


def main():
    print("=" * 70)
    print("SISTEMA DE PLANEJAMENTO - TESTE INTERATIVO")
    print("=" * 70)
    
    # Leitura de parâmetros do usuário
    print("\n📍 Digite os parâmetros do mapa:\n")
    
    goal_x = ler_entrada_float("Coordenada X do objetivo: ")
    goal_y = ler_entrada_float("Coordenada Y do objetivo: ")
    n_obstaculos = ler_entrada_int("Quantidade de triângulos (obstáculos): ")
    tamanho_triangulo = ler_entrada_float("Tamanho dos lados dos triângulos: ")
    
    print()
    print(f"Inicio: (0.0, 0.0)")
    print(f"Objetivo: ({goal_x}, {goal_y})")
    print(f"Obstáculos: {n_obstaculos}")
    print(f"Tamanho triângulos: {tamanho_triangulo}")
    
    # Estatísticas
    total_colisoes_testadas = 0
    total_colisoes_encontradas = 0
    
    # Teste 1: Gerar obstáculos
    print("\n" + "=" * 70)
    print("[1] GERANDO OBSTÁCULOS...")
    print("=" * 70)
    
    try:
        obstaculos = Triangulo.gerar_obstaculos(goal_x, goal_y, n_obstaculos, tamanho_triangulo)
        print(f"✅ {len(obstaculos)} obstáculos gerados com sucesso!")
        
        # Mostrar coordenadas dos obstáculos
        print("\nCoordenadas dos obstáculos:")
        for i, obs in enumerate(obstaculos):
            linhas = pegar_linhas(obs)
            print(f"  Triângulo {i+1}: {linhas}")
        
        # Plotar mapa
        print("\n📊 Gerando visualização...")
        plotar_mapa(goal_x, goal_y, obstaculos)
        
    except Exception as e:
        print(f"❌ Erro ao gerar obstáculos: {e}")
        return
    
    # Teste 2: Verificar colisões entre obstáculos
    print("\n" + "=" * 70)
    print("[2] VERIFICANDO COLISÕES ENTRE OBSTÁCULOS...")
    print("=" * 70)
    
    colisoes_encontradas = 0
    for i in range(len(obstaculos)):
        for j in range(i+1, len(obstaculos)):
            total_colisoes_testadas += 1
            if testar_colisao(obstaculos[i], obstaculos[j]):
                print(f"⚠️  Colisão detectada entre triângulo {i+1} e {j+1}")
                colisoes_encontradas += 1
                total_colisoes_encontradas += 1
    
    if colisoes_encontradas == 0:
        print("✅ Nenhuma colisão entre obstáculos!")
    else:
        print(f"❌ {colisoes_encontradas} colisão(ões) detectada(s)")
    
    # Teste 3: Teste de colisão com triângulo manual
    print("\n" + "=" * 70)
    print("[3] TESTE DE COLISÃO COM TRIÂNGULO MANUAL")
    print("=" * 70)
    
    
    # Resumo final com estatísticas
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS FINAIS")
    print("=" * 70)
    
    if total_colisoes_testadas > 0:
        taxa_colisao = (total_colisoes_encontradas / total_colisoes_testadas) * 100
        barra_colisoes = "█" * int(taxa_colisao / 5) + "░" * (20 - int(taxa_colisao / 5))
        print(f"\n  Testes de colisão realizados: {total_colisoes_testadas}")
        print(f"  Colisões encontradas: {total_colisoes_encontradas}")
        print(f"  Taxa de colisão: {taxa_colisao:.1f}%")
        print(f"  [{barra_colisoes}]")
    else:
        print(f"\n  Nenhum teste de colisão realizado")
    
    print("\n" + "=" * 70)
    print("TESTE FINALIZADO ✨")
    print("=" * 70)


if __name__ == "__main__":
    main()
