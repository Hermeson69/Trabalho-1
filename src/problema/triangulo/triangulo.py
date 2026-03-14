import math as m

import random as rn

from problema.triangulo.utils import Utils

class Triangulo:

    def __init__(self):
        """
        Lista de adjacências para representar o grafo do triângulo. Cada vértice é uma chave no dicionário, e o valor é uma lista de vértices adjacentes.
        """
        self.adj = {}

    def vertice(self,a,b):

        if a not in self.adj:
            self.adj[a] = []

        if b not in self.adj:
            self.adj[b] = []
        
        if b not in self.adj[a]:
            self.adj[a].append(b)

        if a not in self.adj[b]:
            self.adj[b].append(a)
    
    def get_arestas(self):
        """Retorna as arestas do triângulo."""
        arestas = []
        visited = set()
        
        for point_a in self.adj:
            for point_b in self.adj[point_a]:
                aresta = tuple(sorted((point_a, point_b)))
                if aresta not in visited:
                    visited.add(aresta)
                    arestas.append(aresta)
        
        return arestas

    @staticmethod
    def gerar_triangulo(x,y, side):
        """
        Gerar um triângulo equilátero com um vértice em (x, y) e lados de comprimento 'side'.
        """
        # Cálculo dos vértices do triângulo
        height = (m.sqrt(3) / 2) * side
        v1 = (x, y)
        v2 = (x + side, y)
        v3 = (x + side / 2, y + height)

        # Adicionar os vértices ao grafo
        triangulo = Triangulo()
        triangulo.vertice(v1, v2)
        triangulo.vertice(v2, v3)
        triangulo.vertice(v3, v1)

        return triangulo


    """
    Gerar n triângulos aleatórios dentro de uma área definida por (0, 0) a (goal_x, goal_y), garantindo que eles não colidam entre si.
    Cada triângulo é gerado com um vértice em uma posição aleatória e lados de comprimento 'side'.
    """
    @staticmethod
    def gerar_obstaculos(goal_x, goal_y, n, side):
        
        def triangulo_dentro_limites(triangulo, goal_x, goal_y):
            """Verifica se todos os vértices do triângulo estão dentro dos limites."""
            for vertex in triangulo.adj.keys():
                if vertex[0] < 0 or vertex[0] > goal_x or vertex[1] < 0 or vertex[1] > goal_y:
                    return False
            return True
        
        obstaculos = []
        max_tentativas = 1000  # Limite de tentativas para evitar loop infinito

        for _ in range(n):
            tentativas = 0
            while tentativas < max_tentativas:
                tentativas += 1
                
                x = rn.uniform(0, goal_x - side)
                y = rn.uniform(0, goal_y - side)
                triangulo = Triangulo.gerar_triangulo(x, y, side)

                if not triangulo_dentro_limites(triangulo, goal_x, goal_y):
                    continue
                
                # Testar colisão
                valid = True
                for obs in obstaculos:
                    if Utils.testar_colisao(triangulo, obs):
                        valid = False
                        break
                
                if valid:
                    obstaculos.append(triangulo)
                    break
            
            if tentativas >= max_tentativas:
                print(f"⚠️  Aviso: Só foi possível gerar {len(obstaculos)} de {n} obstáculos sem colisão.")
                break
        
        return obstaculos
     
