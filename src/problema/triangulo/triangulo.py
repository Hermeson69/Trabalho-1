import math as m

import random as rn

from problema.triangulo.utils import Utils

class Triangulo:

    def __init__(self):
        """
        Lista de adjacências para representar o grafo do triângulo. Cada vértice é uma chave no dicionário, e o valor é uma lista de vértices adjacentes.
        """
        self.adj = {}
        self.cx = None  # Centro X (pré-calculado)
        self.cy = None  # Centro Y (pré-calculado)
        self.raio = None  # Raio do círculo envolvente (pré-calculado)

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
    def calcular_raio_envolvente(side):
        """Calcula raio do círculo que envolve um triângulo equilátero."""
        return side / m.sqrt(3)

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
        
        triangulo.cx = (v1[0] + v2[0] + v3[0]) / 3
        triangulo.cy = (v1[1] + v2[1] + v3[1]) / 3
        triangulo.raio = Triangulo.calcular_raio_envolvente(side)

        return triangulo


    """
    Gerar n triângulos aleatórios dentro de uma área definida por (0, 0) a (goal_x, goal_y), garantindo que eles não colidam entre si.
    Cada triângulo é gerado com um vértice em uma posição aleatória e lados de comprimento 'side'.
    """
    @staticmethod
    def gerar_obstaculos(goal_x, goal_y, n, side):
        
        obstaculos = []
        quant_colisoes = 0
        
        # Limite baseado nas dimensões do mapa
        max_tentativas_por_obstaculo = int(goal_x * 2)
        
        for i in range(n):
            tentativas_locais = 0
            
            while tentativas_locais < max_tentativas_por_obstaculo:
                tentativas_locais += 1
                
                x = rn.uniform(0, goal_x - side)
                y = rn.uniform(0, goal_y - side)
                triangulo = Triangulo.gerar_triangulo(x, y, side)
                
                # PRÉ-FILTRO DE COLISÃO: Teste de círculos envolventes apenas
                valid = True
                for obs in obstaculos:
                    # Distância entre centros
                    dist_centros_quad = (triangulo.cx - obs.cx) ** 2 + (triangulo.cy - obs.cy) ** 2
                    soma_raios_quad = (triangulo.raio + obs.raio) ** 2
                    
                    # Se círculos NÃO colidem, triângulos também não colidem
                    if dist_centros_quad >= soma_raios_quad:
                        continue
                    
                    # Só faz teste de colisão completo se círculos colidem
                    if Utils.testar_colisao(triangulo, obs):
                        valid = False
                        quant_colisoes += 1
                        break
                
                if valid:
                    obstaculos.append(triangulo)
                    break
            
            if tentativas_locais >= max_tentativas_por_obstaculo:
                print(f"Aviso: Só foi possível gerar {len(obstaculos)} de {n} obstáculos sem colisão.")
                break
        
        print(f"Colisões detectadas: {quant_colisoes}")
        print(f"Obstáculos inseridos: {len(obstaculos)}")
        
        return obstaculos
     
