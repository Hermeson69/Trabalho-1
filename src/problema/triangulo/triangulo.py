import math as m

import random as rn

from problema.triangulo.utils import Utils

class Triangulo:

    def __init__(self):
        """
        Lista de adjacências para representar o grafo do triângulo. Cada vértice é uma chave no dicionário, e o valor é uma lista de vértices adjacentes.
        """
        self.adj = {}
        self.x = None  # Posição X do vértice inicial (pré-calculado)
        self.y = None  # Posição Y do vértice inicial (pré-calculado)
        self.side = None  # Tamanho do lado (pré-calculado)

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
        
        for ponto_a in self.adj:
            for ponto_b in self.adj[ponto_a]:
                aresta = tuple(sorted((ponto_a, ponto_b)))
                if aresta not in visited:
                    visited.add(aresta)
                    arestas.append(aresta)
        
        return arestas

    @staticmethod
    def calcular_raio_envolvente(side):
        """Calcula raio do círculo que envolve um triângulo equilátero."""
        return side / m.sqrt(3)

    @staticmethod
    def ponto_no_triangulo(px, py, x0, y0, side):
        """
        Testa se um ponto (px, py) está dentro de um triângulo equilátero.
        Usa método de semi-planos (3 desigualdades).
        """
        h = m.sqrt(3)
        
        # Base: y >= y0
        if py < y0:
            return False
        
        # Lado esquerdo: y <= sqrt(3) * (x - x0) + y0
        if py > h * (px - x0) + y0:
            return False
        
        # Lado direito: y <= -sqrt(3) * (x - (x0 + side)) + y0
        if py > -h * (px - (x0 + side)) + y0:
            return False
        
        return True

    def get_vertices(self):
        """Retorna os 3 vértices do triângulo."""
        return list(self.adj.keys())

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
        
        # Pré-calcular posição e tamanho (para teste de semi-planos)
        triangulo.x = x
        triangulo.y = y
        triangulo.side = side

        return triangulo


    """
    Gerar n triângulos aleatórios dentro de uma área definida por (0, 0) a (goal_x, goal_y), garantindo que eles não colidam entre si.
    Cada triângulo é gerado com um vértice em uma posição aleatória e lados de comprimento 'side'.
    """
    @staticmethod
    def gerar_obstaculos(goal_x, goal_y, n, side):
        
        obstaculos = []
        quant_colisoes = 0
        quant_rejeitados = 0
        quant_tentativas = 0
        
        # Limite baseado nas dimensões do mapa
        max_tentativas_por_obstaculo = int(goal_x * 2)
        
        for i in range(n):
            tentativas_locais = 0
            
            while tentativas_locais < max_tentativas_por_obstaculo:
                tentativas_locais += 1
                quant_tentativas += 1
                
                x = rn.uniform(0, goal_x - side)
                y = rn.uniform(0, goal_y - side)
                triangulo = Triangulo.gerar_triangulo(x, y, side)
                
                # TESTE DE SEMI-PLANOS: Verifica se vértices estão dentro de outro triângulo
                valid = True
                for obs in obstaculos:
                    # Testa vértices do novo triângulo dentro do existente
                    for vx, vy in triangulo.get_vertices():
                        if Triangulo.ponto_no_triangulo(vx, vy, obs.x, obs.y, obs.side):
                            valid = False
                            quant_colisoes += 1
                            quant_rejeitados += 1
                            break
                    
                    if not valid:
                        break
                    
                    # Testa vértices do existente dentro do novo
                    for vx, vy in obs.get_vertices():
                        if Triangulo.ponto_no_triangulo(vx, vy, triangulo.x, triangulo.y, triangulo.side):
                            valid = False
                            quant_colisoes += 1
                            quant_rejeitados += 1
                            break
                    
                    if not valid:
                        break
                
                if valid:
                    obstaculos.append(triangulo)
                    break
            
            if tentativas_locais >= max_tentativas_por_obstaculo:
                print(f"Aviso: Não foi possível gerar triângulo {i+1}/{n}.")
                break

        print(f"\n{'='*60}")
        print(f"ESTATÍSTICAS DA GERAÇÃO")
        print(f"{'='*60}")
        print(f"Triângulos solicitados: {n}")
        print(f"Triângulos inseridos: {len(obstaculos)}")
        print(f"Triângulos rejeitados: {quant_rejeitados}")
        print(f"Total de tentativas: {quant_tentativas}")
        print(f"Colisões detectadas: {quant_colisoes}")
        print(f"Taxa de sucesso: {(len(obstaculos)/n*100):.1f}%")
        print(f"{'='*60}\n")
        
        return obstaculos
     
