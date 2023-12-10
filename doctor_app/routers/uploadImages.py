import os
import shutil
from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    responses={404: {"description": "Not found"}}
)

paciente = 'paciente1'
path = os.path.abspath(os.path.join('G:', 'Mi unidad', 'pruebasAgendado', paciente, 'img'))


@router.post("/image")
async def image(image: UploadFile = File(...)):
    print(image.filename)

    # Asegurar que el directorio de destino exista
    os.makedirs(path, exist_ok=True)

    # Usar rutas absolutas
    source = os.path.abspath(os.path.join("doctor_app/routers/img", image.filename))
    destination = os.path.join(path, image.filename)

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    uploadimage(source, destination)
    return {"filename": image.filename}


def uploadimage(source, destination):
    try:
        shutil.move(source, destination)
    except FileNotFoundError:
        print(f"El archivo {source} no se pudo encontrar.")
    except Exception as e:
        print(f"Ocurrió un error al mover el archivo: {e}")
