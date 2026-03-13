from problema.triangulo.utils import Utils
from problema.triangulo.triangulo import Triangulo

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
    lines_t1 = pegar_linhas(triangulo1)
    lines_t2 = pegar_linhas(triangulo2)

    for line1 in lines_t1:
        for line2 in lines_t2:
            if Utils.verifica_linhas(line1[0], line1[1], line2[0], line2[1]):
                return True
    return False


def main():
    print("Testando as funcoes:\n")

    t1 = Triangulo()
    A1, B1, C1 = (0, 0), (2, 0), (1, 1.73)
    t1.vertice(A1, B1)
    t1.vertice(B1, C1)
    t1.vertice(C1, A1)

    t2 = Triangulo()
    A2, B2, C2 = (10, 10), (12, 10), (11, 11.73)
    t2.vertice(A2, B2)
    t2.vertice(B2, C2)
    t2.vertice(C2, A2)

    bateram = testar_colisao(t1, t2)

    if bateram:
        print('ocorreu uma colisao.')
    else:
        print('nao ocorreu colisao, triangulo encaixado.')

if __name__ == "__main__":

    main()
