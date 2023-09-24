from fastapi import FastAPI
import mook
app= FastAPI()

@app.get("/")
def root(): 
    return{
        "Servicio": "El más eficiente",
        "El que lea esto" : "le deseo lo mejor"
    }

#Buscador de palabra en los indices invertirdos
@app.post("/indices-invertidos")
def indeces_invertidos(palabra: dict): 
    """_summary_

    Args:
        palabra (dict): Recibe un dicconario con la llave "palabra" y el valor la palabra a buscar

    Returns:
        list: la lista de documentos donde aparece la palabra buscada
    """
    return mook.cache.get(palabra["palabra"], "No se encontro")


#Devuelve un repetido de una lista
@app.post("/numero-repetido")
def numeros_repetidos(lista: dict): 
    return {"repetido":mook.detectar_primer_repetido(lista.get('lista'))}
