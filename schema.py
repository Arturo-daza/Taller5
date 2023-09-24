from pydantic import BaseModel
# Define un modelo Pydantic para el cuerpo de la solicitud
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