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