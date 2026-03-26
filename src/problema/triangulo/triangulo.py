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
    
    def vertices(self):
        """Alias para get_vertices()."""
        return self.get_vertices()

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

        for _ in range(n):
            while True:
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
                            break
                    
                    if not valid:
                        break
                    
                    # Testa vértices do existente dentro do novo
                    for vx, vy in obs.get_vertices():
                        if Triangulo.ponto_no_triangulo(vx, vy, triangulo.x, triangulo.y, triangulo.side):
                            valid = False
                            break
                    
                    if not valid:
                        break
                
                if valid:
                    obstaculos.append(triangulo)
                    break
        
        return obstaculos


class PlanejadorCaminhos:
    """Classe para planejamento de caminhos usando grafo de visibilidade."""
    
    def __init__(self, largura, altura, obstaculos):
        """Inicializa o planejador de caminhos."""
        self.largura = largura
        self.altura = altura
        self.obstaculos = obstaculos
    
    def visivel(self, p1, p2):
        """Verifica se existe linha visível entre p1 e p2."""
        for tri in self.obstaculos:
            verts = tri.vertices()
            arestas = [(verts[0], verts[1]), (verts[1], verts[2]), (verts[2], verts[0])]
            
            # Testa interseção com cada aresta do obstáculo
            for v1, v2 in arestas:
                if Utils.verifica_linhas(p1, p2, v1, v2):
                    return False
            
            # Testa se o ponto médio do segmento está dentro do triângulo
            mx = (p1[0] + p2[0]) / 2.0
            my = (p1[1] + p2[1]) / 2.0
            if Utils.ponto_dentro_triangulo((mx, my), verts):
                return False
        
        return True
    
    def construir_grafo_visibilidade(self, incluir_inicial_final=True):
        """Constrói o grafo de visibilidade entre vértices."""
        vertices = []
        arestas_mesmo_triangulo = set()
        
        # Coleta todos os vértices dos obstáculos
        for tri in self.obstaculos:
            verts = tri.vertices()
            vertices.extend(verts)

            # Marca as 3 arestas do próprio triângulo para não serem usadas no caminho
            if len(verts) >= 3:
                arestas_mesmo_triangulo.add(tuple(sorted((verts[0], verts[1]))))
                arestas_mesmo_triangulo.add(tuple(sorted((verts[1], verts[2]))))
                arestas_mesmo_triangulo.add(tuple(sorted((verts[2], verts[0]))))
        
        # Adiciona início e fim se solicitado
        inicio = (0.0, 0.0)
        fim = (float(self.largura), float(self.altura))
        
        if incluir_inicial_final:
            vertices.append(inicio)
            vertices.append(fim)
        else:
            inicio = fim = None
        
        # Remove duplicados
        uniq = []
        seen = set()
        for v in vertices:
            if v not in seen:
                seen.add(v)
                uniq.append(v)
        
        # Constrói o grafo
        grafo = {v: [] for v in uniq}
        
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                p1, p2 = uniq[i], uniq[j]

                if tuple(sorted((p1, p2))) in arestas_mesmo_triangulo:
                    continue

                if self.visivel(p1, p2):
                    dist = m.hypot(p1[0] - p2[0], p1[1] - p2[1])
                    grafo[p1].append((p2, dist))
                    grafo[p2].append((p1, dist))
        
        return grafo, inicio, fim

    def buscar_caminho_qualquer(self, grafo, inicio, fim):
        """Retorna qualquer caminho entre inicio e fim usando DFS (não ótimo)."""
        if inicio not in grafo or fim not in grafo:
            return None

        visitados = set()
        pilha = [(inicio, [inicio])]

        while pilha:
            atual, caminho = pilha.pop()

            if atual == fim:
                return caminho

            if atual in visitados:
                continue
            visitados.add(atual)

            for vizinho, _ in grafo[atual]:
                if vizinho not in visitados:
                    pilha.append((vizinho, caminho + [vizinho]))

        return None
    
    # def busca_a_estrela(self, grafo, inicio, fim):
    #     """Busca A* para encontrar caminho ótimo entre inicio e fim."""
    #     if inicio not in grafo or fim not in grafo:
    #         return None
    #     open_set = [(0, inicio, [inicio])]
    #     g_costs = {inicio: 0}

    #     while open_set:
    #         _, atual, caminho = open_set.pop(0)

    #         if atual == fim:
    #             return caminho

    #         for vizinho, dist in grafo[atual]:
    #             tentative_g_cost = g_costs[atual] + dist
    #             if vizinho not in g_costs or tentative_g_cost < g_costs[vizinho]:
    #                 g_costs[vizinho] = tentative_g_cost
    #                 f_cost = tentative_g_cost + m.hypot(vizinho[0] - fim[0], vizinho[1] - fim[1])
    #                 open_set.append((f_cost, vizinho, caminho + [vizinho]))
    #                 open_set.sort(key=lambda x: x[0])
    #     return None
        

