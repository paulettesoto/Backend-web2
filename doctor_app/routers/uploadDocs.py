#G:\Mi unidad\pruebasAgendado
import shutil
import os
from fastapi import APIRouter, File, UploadFile


router = APIRouter()
paciente = 'paciente1'
path = 'G:/Mi unidad/pruebasAgendado/'+paciente+'/'+'docs'
@router.post("/pdf")
async def pdf(pdf: UploadFile = File(...)):
    print(pdf.filename)
    with open("doctor_app/routers/docs/"+pdf.filename, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)
    uploadimage(path, pdf.filename)
    return {"filename": pdf.filename}


def uploadimage(path, file):
    try:
        os.mkdir(path)
        source = "doctor_app/routers/docs/" + file

        # Destination path
        destination = path + "/" + file

        # Move the content of
        # source to destination
        shutil.move(source, destination)
    except OSError as error:
        print(error)
