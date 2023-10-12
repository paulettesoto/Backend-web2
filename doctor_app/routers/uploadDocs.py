#G:\Mi unidad\pruebasAgendado
import shutil
import os
from fastapi import APIRouter, File, UploadFile, Depends
#from ..dependecies import get_token_header


router = APIRouter(
    prefix="/uploadFiles",
    tags=["Guardar archivos"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


paciente = 'paciente1'
path = 'G:/Mi unidad/pruebasAgendado/'+paciente+'/'+'docs'


@router.post("/docs")
async def docs(docs: UploadFile = File(...)):
    print(docs.filename)
    with open("doctor_app/routers/docs/"+docs.filename, "wb") as buffer:
        shutil.copyfileobj(docs.file, buffer)
    uploaddoc(path, docs.filename)
    return {"filename": docs.filename}


def uploaddoc(path, file):
    #try:
        #os.mkdir(path)
    source = "doctor_app/routers/docs/" + file

        # Destination path
    destination = path + "/" + file

        # Move the content of
        # source to destination
    shutil.move(source, destination)
    #except OSError as error:
        #print(error)
