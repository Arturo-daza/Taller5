from fastapi import FastAPI
import mook
app= FastAPI()

@app.get("/")
def root(): 
    return{
        "Servicio": "Estructura de datos"
    }

#Buscador de palabra en los indices invertirdos
@app.post("/indices-invertidos")
def indeces_invertidos(palabra: dict): 
    #logica del codigo
    return mook.cache.get(palabra["palabra"], "No se encontro")
