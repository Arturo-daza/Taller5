from fastapi import FastAPI, Request, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder

import schema
import mook
import arbol_binario as ab
from grafo import Grafo
import boto3
from concurrent.futures import ThreadPoolExecutor
import time
from io import StringIO
from nn import imputacion
import pandas as pd


templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Lista para almacenar las conexiones WebSocket
connections = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Aceptar la conexión WebSocket
    connections.add(websocket)  # Añadir la conexión WebSocket a la lista
    try:
        while True:
            # Recibir mensajes del cliente WebSocket
            data = await websocket.receive_text()
            print(f"Mensaje recibido: {data}")

            # Enviar mensajes a todos los clientes WebSocket conectados
            for connection in connections:
                await connection.send_text(f"Mensaje recibido: {data}")
    except Exception as e:
        print(f"Error en la conexión WebSocket: {e}")
    finally:
        # Remover la conexión WebSocket de la lista cuando se cierra la conexión
        connections.remove(websocket)
# Ruta de prueba para servir la página HTML que usa el WebSocket
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>WebSocket Test</title>
        </head>
        <body>
            <h1>WebSocket Test</h1>
            <script>
                const socket = new WebSocket("ws://" + window.location.host + "/ws");

                socket.onmessage = (event) => {
                    console.log("Mensaje recibido:", event.data);
                };

                socket.onclose = (event) => {
                    console.error("WebSocket cerrado:", event);
                };

                function sendMessage() {
                    const message = document.getElementById("message").value;
                    socket.send(message);
                }
            </script>
            <input type="text" id="message" placeholder="Escribe un mensaje" />
            <button onclick="sendMessage()">Enviar</button>
        </body>
    </html>
    """

aws_access_key_id = 'AKIAYEIE6WITLXIU6YWL'
aws_secret_access_key = '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'
queue_url = 'https://sqs.us-east-2.amazonaws.com/558893019686/LaMasVeloz'

sqs = boto3.client(
    'sqs',
    region_name='us-east-2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


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

@app.post("/api/sqs")
def publicar(message:dict):
    # Publicar un mensaje en la cola
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message['message']
    )

    print(f'Mensaje publicado con éxito: {response["MessageId"]}')
    return {"id": response["MessageId"]}






def process_messages(processed_messages, processed_count):
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=0
        )

        if 'Messages' in response and len(response['Messages']) > 0:
            message = response['Messages'][0]
            print(f"Mensaje recibido: {message['Body']}")

            # Añadir el mensaje a la lista de mensajes procesados
            processed_messages.append(message['Body'])
            # Incrementar el contador de mensajes procesados
            processed_count[0] += 1

            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
        else:
            print("No se encontraron mensajes en la cola.")
            break

@app.get("/api/sqs")
async def process_sqs_messages():
    # Lista para almacenar los mensajes procesados
    processed_messages = []
    # Contador de mensajes procesados
    processed_count = [0]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=30) as executor:
        for _ in range(30):
            executor.submit(process_messages, processed_messages, processed_count)

    end_time = time.time()
    elapsed_time = end_time - start_time
    return {
        "Tiempo transcurrido para procesar mensajes": f"{elapsed_time} segundos",
        "Mensajes procesados": processed_count[0],
        "Lista de mensajes procesados": processed_messages
    }
    
@app.post("/imputacion")
async def imputacion_nn(file: UploadFile = File(...)):
    contents = file.file.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))
    describe_data_original= df.describe().to_dict()
    print(df.isnull().sum())
    df_imputed=imputacion(df)
    df_imputed_dict = df_imputed.to_dict() # Convertir el dataframe a un diccionario
    describe_data_imputed = df_imputed.describe().to_dict()
    response = {
        "data": jsonable_encoder(df_imputed_dict),  # Devolver el diccionario como una respuesta JSON
        "describe_imputed": jsonable_encoder(describe_data_imputed), 
        "describe_original":  jsonable_encoder(describe_data_original)
        
    }
    return response

    
    
    
    
    
# @app.get('/indices-invertidos')
# def indices_invertidos(request:Request):
#     return templates.TemplateResponse("indices-invertidos.html", {"request":request})


# @app.get('/')
# def indices_invertidos(request:Request):
#     return templates.TemplateResponse("index.html", {"request":request})