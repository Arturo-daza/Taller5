from collections import defaultdict, deque
import networkx as nx


class Grafo:
    def __init__(self):
        self.grafo = defaultdict(list)

    def agregar_arista(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)

    def bfs(self, inicio, destino):
        visitados = set()
        cola = deque()
        cola.append((inicio, [inicio]))
        while cola:
            nodo, camino = cola.popleft()

            if nodo == destino:
                return camino

            if nodo not in visitados:
                visitados.add(nodo)

                for vecino in self.grafo[nodo]:
                    if vecino not in visitados:
                        nuevo_camino = list(camino)
                        nuevo_camino.append(vecino)
                        cola.append((vecino, nuevo_camino))
        return None

    def dfs(self, inicio, destino):
        visitados = set()
        pila = [(inicio, [inicio])]
        while pila:
            (nodo, camino) = pila.pop()

            if nodo not in visitados:
                if nodo == destino:
                    return camino

                visitados.add(nodo)

                for vecino in self.grafo[nodo]:
                    if vecino not in visitados:
                        nuevo_camino = list(camino)
                        nuevo_camino.append(vecino)
                        pila.append((vecino, nuevo_camino))
        return None

