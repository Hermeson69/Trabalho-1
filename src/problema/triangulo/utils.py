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
    

    def verifica_linhas(a1, b1, a2, b2):
        o1 = Utils.orientacao(a1, b1, a2)
        o2 = Utils.orientacao(a1, b1, b2)
        o3 = Utils.orientacao(a2, b2, a1)
        o4 = Utils.orientacao(a2, b2, b1)

        if (((o1 < 0 and o2 < 0) or (o1 > 0 and o2 > 0))
            or ((o3 < 0 and o4 < 0) or (o3 > 0 and o4 > 0))):
            return False
        elif (o1 * o2 < 0) and (o3 * o4 < 0):
            return True

        if (o1 == 0 and Utils.no_segmento(a1, a2, b1)):
            return True
        if (o2 == 0 and Utils.no_segmento(a1, b2, b1)):
            return True
        if (o3 == 0 and Utils.no_segmento(a2, a1, b2)):
            return True
        if (o4 == 0 and Utils.no_segmento(a2, b1, b2)):
            return True
        return False