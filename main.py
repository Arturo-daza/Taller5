from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import schema
import mook
import arbol_binario as ab
from grafo import Grafo
import threading
from sqs import process_messages as pm
import sqs
templates = Jinja2Templates(directory="templates")

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIS
@app.get("/api/")
def root():
    return {
        "Servicio": "Estructura de datos",
        "Lista para la busqueda": mook.my_documents
    }

# Buscador de palabra en los indices invertirdos
@app.post("/api/indices-invertidos", response_model=schema.ResultadoBusqueda)
def indices_invertidos(palabra: schema.PalabraBuscar):
    """
    Endpoint que recibe una palabra y devuelve el documento si existe en la caché.

    Args:
        palabra: Objeto que contiene la palabra a buscar.

    Returns:
        str: El/Los documentos de la palabra si se encuentra en la caché, de lo contrario "No se encontro".
    """

    return {"resultado": mook.cache.get(palabra.palabra, ["No se encontro"])}   


# Devuelve un repetido de una lista
@app.post("/api/numero-repetido", response_model=schema.NumeroRepetido)
def numeros_repetidos(lista: schema.ListaNumeros):
    """
    Detecta el primer número repetido en una lista.

    El array contiene números en el rango de 1 a n, donde n es la longitud del array.

    Args:
        lista (dict): Un diccionario que contiene una lista de enteros bajo la clave 'lista'.

    Returns:
        dict: Un diccionario que contiene el primer número repetido bajo la clave 'repetido'.
    """
    
    return {"repetido": mook.detectar_primer_repetido(lista.lista)}


@app.post("/api/merge-sort", response_model=schema.ResultadoMergeSort)
def merge_sort(lista: schema.ListaMergeSort):
    """
    Ordena una lista de cadenas de texto utilizando el algoritmo de ordenamiento merge sort.

    Args:
        lista (dict): Un diccionario que contiene una lista de cadenas de texto bajo la clave 'lista'.

    Returns:
        dict: Un diccionario que contiene la lista de cadenas de texto ordenada bajo la clave 'organizado'.
    """
    return {"organizado": mook.merge_sort(lista.lista)}

# Templates

#Generación de arbol binario según una lista
@app.post("/api/arbol-binario", response_model = schema.EsquemaArbol)
def arbol_binario(lista: schema.ListaNumeros):
    """
    Crea un árbol binario de búsqueda a partir de una lista de números y devuelve su representación en formato JSON,
    junto con sus recorridos en preorden, inorder y postorden.

    Args:
        lista: Una instancia de schema.ListaNumeros que contiene la lista de números a insertar en el árbol.

    Returns:
        Un diccionario con las siguientes claves:
            - "arbol": La representación en formato JSON del árbol binario de búsqueda creado.
            - "preorden": Una lista con los valores del árbol en recorrido preorden.
            - "inorder": Una lista con los valores del árbol en recorrido inorder.
            - "postorden": Una lista con los valores del árbol en recorrido postorden.
    """
    arbol = ab.ArbolBinarioBusqueda()
    for valor in lista.lista:
        arbol.insertar(valor)
    salida = arbol.imprimir_arbol_json()
    preorden = arbol.preorden()
    inorder = arbol.inorder()
    postorden = arbol.postorden()
    return {
        "arbol": salida,
        "preorden": preorden,
        "inorder": inorder,
        "postorden": postorden
        }

@app.post("/api/grafo", response_model= schema.Camino)
def grafo(grafo_buscar: schema.Grafo):
    """
    Esta función recibe un objeto de grafo y devuelve un diccionario que contiene el grafo,
    el resultado de una búsqueda en anchura (breadth-first search) y el resultado de una búsqueda en profundidad (depth-first search).
    
    Args:
    grafo_buscar: Un objeto de grafo que contiene el grafo a ser buscado y la ruta a ser encontrada.    
    Returns:
    Un diccionario que contiene el grafo, el resultado de una búsqueda en anchura y el resultado de una búsqueda en profundidad.    """
    grafo = Grafo()
    print(grafo_buscar)
    for arista in grafo_buscar.aristas:
        grafo.agregar_arista(*arista)
    bfs=grafo.bfs(grafo_buscar.camino[0], grafo_buscar.camino[1])
    dfs = grafo.dfs(grafo_buscar.camino[0], grafo_buscar.camino[1])
    
    return {"grafo": dict(grafo.grafo), "bfs": bfs, "dfs":dfs}

# @app.post("/api/sqs")
# def publicar(message:dict):
#         # Publicar un mensaje en la cola
#     response = sqs.send_message(
#         QueueUrl=queue_url,
#         MessageBody=message['message']
#     )

    print(f'Mensaje publicado con éxito: {response["MessageId"]}')
    return {"id": response["MessageId"]}

response=[]
@app.get("/api/sqs")
def process():
    
    for i in range(10):
        threading.Thread(target=pm).start()
    print(sqs.processed_messages)
    response.extend(sqs.processed_messages)
    print(response)
    return {
        "total mensajes procesados" : len(response),
        "mensajes leidos": response
        }
@app.get("/api/sqs_clean")
def clean_response():
    return {"mensajes": response.clear()}