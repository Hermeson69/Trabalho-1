class Utils:

    def orientacao(a, b, c):
        """Função para calcular a orientação de três pontos (a, b, c). Retorna um valor positivo se os pontos estão em sentido anti-horário, negativo se estão em sentido horário e zero se são colineares."""
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])