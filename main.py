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
    #logica del codigo
    return mook.cache.get(palabra["palabra"], "No se encontro")


#Devuelve un repetido de una lista
@app.post("/numero-repetido")
def indeces_invertidos(lista: dict): 
    
    return {"repetido":mook.detectar_primer_repetido(lista.get('lista'))}
