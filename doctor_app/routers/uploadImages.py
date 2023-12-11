import os
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    responses={404: {"description": "Not found"}}
)



@router.post("/image")
async def image(Nombre:str, primerape:str, segundoape:str,tratamiento:str, image: UploadFile = File(...)):
    try:
        paciente = Nombre + '_' + primerape + '_' +segundoape
        # Define la ruta local en Google Drive
        path = os.path.join('G:', 'Mi unidad', 'DoctorApp', paciente,tratamiento)
        destination = os.path.join(path, image.filename)

        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Guarda el archivo en la ruta local
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return JSONResponse(content={"filename": image.filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
