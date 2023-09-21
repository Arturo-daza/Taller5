from fastapi import FastAPI

app= FastAPI()

@app.get("/")
def root(): 
    return{
        "Servicio": "Estructura de datos"
    }

#Buscador de palabra en los indices invertirdos
@app.post("/indices-invertidos")
def indeces_invertidos(): 
    #logica del codigo
    return {}
