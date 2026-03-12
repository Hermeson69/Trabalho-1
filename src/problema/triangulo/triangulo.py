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

        self.adj[a].append(b)
        self.adj[b].append(a)