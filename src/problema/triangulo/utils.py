class Utils:

    @staticmethod
    def orientacao(a, b, c):
        """Função para calcular a orientação de três pontos (a, b, c). Retorna um valor positivo se os pontos estão em sentido anti-horário, negativo se estão em sentido horário e zero se são colineares."""
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    
    @staticmethod
    def no_segmento(p, q, r):
        """Função para verificar se q está sobre o segmento p-retafim"""

        if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
            return True
        return False
    
    @staticmethod
    def ponto_dentro_triangulo(ponto, tri_vertices):
        """Verifica se um ponto está DENTRO de um triângulo (não na borda)."""
        a, b, c = tri_vertices[0], tri_vertices[1], tri_vertices[2]
        
        o1 = Utils.orientacao(a, b, ponto)
        o2 = Utils.orientacao(b, c, ponto)
        o3 = Utils.orientacao(c, a, ponto)
        
        # Ponto está dentro (exclude bordas) se todas as orientações têm o mesmo sinal (não zero)
        return (o1 > 0 and o2 > 0 and o3 > 0) or (o1 < 0 and o2 < 0 and o3 < 0)

    @staticmethod
    def verifica_linhas(a1, b1, a2, b2, tolerancia=1e-9):
        """Verifica se dois segmentos se interceptam (sem contar apenas toque nas extremidades)."""
        o1 = Utils.orientacao(a1, b1, a2)
        o2 = Utils.orientacao(a1, b1, b2)
        o3 = Utils.orientacao(a2, b2, a1)
        o4 = Utils.orientacao(a2, b2, b1)

        # Casos de interseção clara (não apenas toque)
        if (o1 * o2 < 0) and (o3 * o4 < 0):
            return True
        
        # Não considerar colisão se apenas tocam nas extremidades
        return False
    
    @staticmethod
    def testar_colisao(triangulo1, triangulo2):
        """Testa se dois triângulos colidem verificando interseção de arestas e pontos dentro."""
        arestas_t1 = triangulo1.get_arestas()
        arestas_t2 = triangulo2.get_arestas()
        
        # Verificar interseção de arestas
        for aresta1 in arestas_t1:
            for aresta2 in arestas_t2:
                if Utils.verifica_linhas(aresta1[0], aresta1[1], aresta2[0], aresta2[1]):
                    return True
        
        vertices_t1 = list(triangulo1.adj.keys())
        vertices_t2 = list(triangulo2.adj.keys())
        
        for v1 in vertices_t1:
            if Utils.ponto_dentro_triangulo(v1, vertices_t2):
                return True
        
        for v2 in vertices_t2:
            if Utils.ponto_dentro_triangulo(v2, vertices_t1):
                return True
        
        return False