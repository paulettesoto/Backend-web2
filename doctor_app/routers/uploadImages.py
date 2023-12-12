import os
import shutil
from fastapi import APIRouter, FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    responses={404: {"description": "Not found"}}
)


@router.post("/image")
async def image(Nombre: str = Form(...), primerape: str = Form(...), segundoape: str = Form(...), tratamiento: str = Form(...), image: UploadFile = File(...)):
    try:
        paciente = Nombre + '_' + primerape + '_' + segundoape
        # Define la ruta local en Google Drive
        path = os.path.join('G:', 'Mi unidad', 'DoctorApp', paciente, tratamiento)
        destination = os.path.join(path, image.filename)

        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Guarda el archivo en la ruta local
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        return {"filename": image.filename, "Nombre": Nombre, "tratamiento": tratamiento}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))