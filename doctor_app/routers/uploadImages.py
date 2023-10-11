#G:\Mi unidad\pruebasAgendado
import shutil
import os
from fastapi import APIRouter, File, UploadFile, Depends
from ..dependecies import get_token_header


router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


paciente = 'paciente1'
path = 'G:/Mi unidad/pruebasAgendado/'+paciente+'/img'


@router.post("/image")
async def image(image: UploadFile = File(...)):
    print(image.filename)
    with open("doctor_app/routers/img/"+image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    uploadimage(path, image.filename)
    return {"filename": image.filename}


def uploadimage(path, file):
    #try:
        #os.mkdir(path)
    source = "doctor_app/routers/img/" + file

        # Destination path
    destination = path + "/" + file

        # Move the content of
        # source to destination
    shutil.move(source, destination)
    #except OSError as error:
        #print(error)



