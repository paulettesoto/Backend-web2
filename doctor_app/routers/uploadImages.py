import os
import shutil
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    responses={404: {"description": "Not found"}}
)

paciente = 'paciente1'
# Utiliza el directorio temporal proporcionado por Render
temp_path = os.environ.get("TMPDIR", "/tmp")  # Obtén la ubicación del directorio temporal
final_path = os.path.abspath(os.path.join('G:', 'Mi unidad', 'pruebasAgendado', paciente, 'img'))

@router.post("/image")
async def image(image: UploadFile = File(...)):
    try:
        # Crea un archivo temporal para almacenar el archivo cargado
        with NamedTemporaryFile(delete=False, dir=temp_path) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(image.file, temp_file)

        # Construye la ruta local del archivo en Google Drive
        destination = os.path.join(final_path, image.filename)

        # Asegúrate de que el directorio de destino exista
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Mueve el archivo desde el directorio temporal al destino final
        shutil.move(temp_file_path, destination)

        return JSONResponse(content={"filename": image.filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
