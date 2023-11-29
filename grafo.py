from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt


class Grafo:
    """
    Clase que representa un grafo no dirigido.

    Atributos:
    - grafo: diccionario que contiene las aristas del grafo.
    """

    def __init__(self):
        """
        Inicializa un objeto Grafo con un diccionario vacío.
        """
        self.grafo = defaultdict(list)

    def agregar_arista(self, u, v):
        """
        Agrega una arista al grafo.

        Parámetros:
        - u: vértice origen de la arista.
        - v: vértice destino de la arista.
        """
        self.grafo[u].append(v)
        self.grafo[v].append(u)
    
    def graficar(self):
        G = nx.Graph()
        for u, vecinos in self.grafo.items():
            for v in vecinos:
                G.add_edge(u, v)

        # Obtener la información del grafo en formato JSON
        grafo_json = {
            "nodes": [{"id": str(node)} for node in G.nodes],
            "links": [{"source": str(edge[0]), "target": str(edge[1])} for edge in G.edges],
        }

        return grafo_json


    def bfs(self, inicio, destino):
        """
        Realiza un recorrido BFS (Breadth-First Search) en el grafo.

        Parámetros:
        - inicio: vértice de inicio del recorrido.
        - destino: vértice de destino del recorrido.

        Retorna:
        - El camino desde el vértice de inicio hasta el vértice de destino, si existe.
        - None, si no existe un camino entre los vértices.
        """
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
        """
        Realiza un recorrido DFS (Depth-First Search) en el grafo.

        Parámetros:
        - inicio: vértice de inicio del recorrido.
        - destino: vértice de destino del recorrido.

        Retorna:
        - El camino desde el vértice de inicio hasta el vértice de destino, si existe.
        - None, si no existe un camino entre los vértices.
        """
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

