from pydantic import BaseModel,  Field

class NodoSchema(BaseModel):
    valor: int
    izquierda: 'NodoSchema' = None
    derecha: 'NodoSchema' = None

class EsquemaArbol(BaseModel):
    arbol: NodoSchema
    preorden: list[int]
    inorder: list[int]
    postorden: list[int]

class PalabraBuscar(BaseModel):
    palabra: str = Field(..., example="programación")

class ResultadoBusqueda(BaseModel):
    resultado: list[str]
    
class ListaNumeros(BaseModel):
    lista: list[int] = Field(..., example=[3,2,1,2,4,5,6,0])

class NumeroRepetido(BaseModel):
    repetido: int

class ListaMergeSort(BaseModel):
    lista: list[str] = Field(..., example=["jose", "antonio", "pedro", "ignacio"])

class ResultadoMergeSort(BaseModel):
    organizado: list[str]


class Grafo(BaseModel):
    aristas: list[tuple[int, int]] = Field(..., example= [(0,1), (0,3), (3,4), (3,1), (4,5), (4,2), (0,4)])
    camino: tuple[int, int] = Field(..., example= (0,2))
    
class Camino(BaseModel):
    grafo: dict[int, list[int]]
    bfs: list[int]
    dfs:list[int]
    
    