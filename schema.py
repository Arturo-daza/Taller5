from pydantic import BaseModel

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
    palabra: str

class ResultadoBusqueda(BaseModel):
    resultado: list[str]
    
class ListaNumeros(BaseModel):
    lista: list[int]

class NumeroRepetido(BaseModel):
    repetido: int

class ListaMergeSort(BaseModel):
    lista: list[str]

class ResultadoMergeSort(BaseModel):
    organizado: list[str]
