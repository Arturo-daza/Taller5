from fastapi import FastAPI
import schema
import mook



app= FastAPI()


@app.get("api/")
def root(): 
    return{
        "Servicio": "Estructura de datos",
        "Lista para la busqueda" : mook.my_documents
    }

#Buscador de palabra en los indices invertirdos
@app.post("api/indices-invertidos", response_model=schema.ResultadoBusqueda)
def indices_invertidos(palabra: schema.PalabraBuscar): 
    """
    Endpoint que recibe una palabra y devuelve el documento si existe en la caché.

    Args:
        palabra (schema.PalabraBuscar): Objeto que contiene la palabra a buscar.

    Returns:
        str: El/Los documentos de la palabra si se encuentra en la caché, de lo contrario "No se encontro".
    """
    
    return {"resultado" : mook.cache.get(palabra.palabra, "No se encontro")}


#Devuelve un repetido de una lista
@app.post("api/numero-repetido", response_model=schema.NumeroRepetido)
def numeros_repetidos(lista: schema.ListaNumeros): 
    """
    Detects the first repeated number in a list.

    the array contains numbers that are in the range 1 to n, where n is the length of the array.
    
    Args:
        lista (dict): A dictionary containing a list of integers under the key 'lista'.

    Returns:
        dict: A dictionary containing the first repeated number under the key 'repetido'.
    """
    return {"repetido":mook.detectar_primer_repetido(lista.get('lista'))}


@app.post("api/merge-sort", response_model= schema.ResultadoMergeSort)
def merge_sort(lista: schema.ListaMergeSort):
    """
    Sorts a list of strings using merge sort.

    Args:
        lista (dict): A dictionary containing a list of strings under the key 'lista'.

    Returns:
        dict: A dictionary containing the sorted list of strings under the key 'organizado'.
    """
    return {"organizado":mook.merge_sort(lista.lista)}