import json

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

    
class ArbolBinarioBusqueda:
    """
    A class representing a binary search tree.

    Attributes:
    -----------
    raiz : Nodo
        The root node of the binary search tree.

    Methods:
    --------
    insertar(valor)
        Inserts a new node with the given value into the binary search tree.
    buscar(valor)
        Searches for a node with the given value in the binary search tree.
    imprimir_arbol()
        Prints the binary search tree in a tree-like format.
    imprimir_arbol_json()
        Returns the binary search tree as a dictionary in JSON format.
    preorden()
        Returns a list of the values of the nodes in the binary search tree in pre-order traversal.
    inorder()
        Returns a list of the values of the nodes in the binary search tree in in-order traversal.
    postorden()
        Returns a list of the values of the nodes in the binary search tree in post-order traversal.
    """

    def __init__(self):
        """
        Initializes an empty binary search tree.
        """
        self.raiz = None

    def insertar(self, valor):
        """
        Inserts a new node with the given value into the binary search tree.

        Parameters:
        -----------
        valor : int
            The value of the new node to be inserted.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivamente(valor, self.raiz)

    def _insertar_recursivamente(self, valor, nodo):
        """
        A helper method for insertar() that recursively inserts a new node with the given value into the binary search tree.

        Parameters:
        -----------
        valor : int
            The value of the new node to be inserted.
        nodo : Nodo
            The current node being checked for insertion.
        """
        if valor == nodo.valor:
            # Value already exists in the binary search tree, ignore insertion
            return
        elif valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_recursivamente(valor, nodo.izquierda)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_recursivamente(valor, nodo.derecha)

    def buscar(self, valor):
        """
        Searches for a node with the given value in the binary search tree.

        Parameters:
        -----------
        valor : int
            The value of the node to be searched for.

        Returns:
        --------
        bool
            True if a node with the given value is found, False otherwise.
        """
        if self.raiz is not None:
            return self._buscar_recursivamente(valor, self.raiz)
        else:
            return False

    def _buscar_recursivamente(self, valor, nodo):
        """
        A helper method for buscar() that recursively searches for a node with the given value in the binary search tree.

        Parameters:
        -----------
        valor : int
            The value of the node to be searched for.
        nodo : Nodo
            The current node being checked for the given value.

        Returns:
        --------
        bool
            True if a node with the given value is found, False otherwise.
        """
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor and nodo.izquierda is not None:
            return self._buscar_recursivamente(valor, nodo.izquierda)
        elif valor > nodo.valor and nodo.derecha is not None:
            return self._buscar_recursivamente(valor, nodo.derecha)
        return False

    def imprimir_arbol(self):
        """
        Prints the binary search tree in a tree-like format.
        """
        if self.raiz is not None:
            self._imprimir_arbol_recursivamente(self.raiz, "", True)

    def _imprimir_arbol_recursivamente(self, nodo, prefijo, es_ultimo):
        """
        A helper method for imprimir_arbol() that recursively prints the binary search tree in a tree-like format.

        Parameters:
        -----------
        nodo : Nodo
            The current node being printed.
        prefijo : str
            The prefix string used for indentation.
        es_ultimo : bool
            True if the current node is the last child of its parent, False otherwise.
        """
        if nodo is not None:
            print(prefijo + ("└── " if es_ultimo else "├── ") + str(nodo.valor))
            prefijo += "    " if es_ultimo else "│   "
            self._imprimir_arbol_recursivamente(nodo.izquierda, prefijo, False)
            self._imprimir_arbol_recursivamente(nodo.derecha, prefijo, True)

    def obtener_arbol(self, nodo=None):
        """
        Returns the binary search tree as a dictionary.

        Parameters:
        -----------
        nodo : Nodo, optional
            The current node being added to the dictionary. Defaults to the root node.

        Returns:
        --------
        dict
            The binary search tree as a dictionary.
        """
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return None
        arbol_dic = {
            "valor": nodo.valor,
        }
        if nodo.izquierda is not None:
            arbol_dic["izquierda"] = self.obtener_arbol(nodo.izquierda)
        if nodo.derecha is not None:
            arbol_dic["derecha"] = self.obtener_arbol(nodo.derecha)
        return arbol_dic

    def imprimir_arbol_json(self):
        """
        Returns the binary search tree as a dictionary in JSON format.

        Returns:
        --------
        dict
            The binary search tree as a dictionary in JSON format.
        """
        arbol_dic = self.obtener_arbol()
        return arbol_dic

    def preorden(self):
        """
        Returns a list of the values of the nodes in the binary search tree in pre-order traversal.

        Returns:
        --------
        list
            A list of the values of the nodes in the binary search tree in pre-order traversal.
        """
        result = []
        if self.raiz is not None:
            self._preorden_recursivamente(self.raiz, result)
        return result

    def _preorden_recursivamente(self, nodo, result):
        """
        A helper method for preorden() that recursively adds the values of the nodes in the binary search tree to a list in pre-order traversal.

        Parameters:
        -----------
        nodo : Nodo
            The current node being added to the list.
        result : list
            The list of node values being built.
        """
        if nodo is not None:
            result.append(nodo.valor)
            self._preorden_recursivamente(nodo.izquierda, result)
            self._preorden_recursivamente(nodo.derecha, result)

    def inorder(self):
        """
        Returns a list of the values of the nodes in the binary search tree in in-order traversal.

        Returns:
        --------
        list
            A list of the values of the nodes in the binary search tree in in-order traversal.
        """
        result = []
        if self.raiz is not None:
            self._inorder_recursivamente(self.raiz, result)
        return result

    def _inorder_recursivamente(self, nodo, result):
        """
        A helper method for inorder() that recursively adds the values of the nodes in the binary search tree to a list in in-order traversal.

        Parameters:
        -----------
        nodo : Nodo
            The current node being added to the list.
        result : list
            The list of node values being built.
        """
        if nodo is not None:
            self._inorder_recursivamente(nodo.izquierda, result)
            result.append(nodo.valor)
            self._inorder_recursivamente(nodo.derecha, result)

    def postorden(self):
        """
        Returns a list of the values of the nodes in the binary search tree in post-order traversal.

        Returns:
        --------
        list
            A list of the values of the nodes in the binary search tree in post-order traversal.
        """
        result = []
        if self.raiz is not None:
            self._postorden_recursivamente(self.raiz, result)
        return result

    def _postorden_recursivamente(self, nodo, result):
        """
        A helper method for postorden() that recursively adds the values of the nodes in the binary search tree to a list in post-order traversal.

        Parameters:
        -----------
        nodo : Nodo
            The current node being added to the list.
        result : list
            The list of node values being built.
        """
        if nodo is not None:
            self._postorden_recursivamente(nodo.izquierda, result)
            self._postorden_recursivamente(nodo.derecha, result)
            result.append(nodo.valor)
            
    
