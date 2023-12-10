import os
import shutil
import tempfile
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

    # Usar un directorio temporal
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, image.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Mover el archivo desde el directorio temporal al destino final
        destination = os.path.join(path, image.filename)

        # Utilizar shutil.copy en lugar de shutil.move
        shutil.copy(temp_file_path, destination)

        return {"filename": image.filename}
    finally:
        # Limpiar el directorio temporal incluso en caso de error
        shutil.rmtree(temp_dir, ignore_errors=True)
