from fastapi import FastAPI
import schema
import mook



app= FastAPI()


@app.get("/")
def root(): 
    return{
        "Servicio": "El más eficiente",
        "El que lea esto" : "le deseo lo mejor"
    }

#Buscador de palabra en los indices invertirdos
@app.post("/indices-invertidos", response_model=schema.ResultadoBusqueda)
def indeces_invertidos(palabra: schema.PalabraBuscar): 
    """
    Endpoint que recibe una palabra y devuelve el documento si existe en la caché.

    Args:
        palabra (schema.PalabraBuscar): Objeto que contiene la palabra a buscar.

    Returns:
        str: El/Los documentos de la palabra si se encuentra en la caché, de lo contrario "No se encontro".
    """
    
    return {"resultado" : mook.cache.get(palabra.palabra, "No se encontro")}


#Devuelve un repetido de una lista
@app.post("/numero-repetido", response_model=schema.NumeroRepetido)
def numeros_repetidos(lista: schema.ListaNumeros): 
    """
    Detects the first repeated number in a list.

    Args:
        lista (dict): A dictionary containing a list of integers under the key 'lista'.

    Returns:
        dict: A dictionary containing the first repeated number under the key 'repetido'.
    """
    return {"repetido":mook.detectar_primer_repetido(lista.get('lista'))}
