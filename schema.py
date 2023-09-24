from pydantic import BaseModel
# Define un modelo Pydantic para el cuerpo de la solicitud
class PalabraBuscar(BaseModel):
    palabra: str

class ResultadoBusqueda(BaseModel):
    resultado: list