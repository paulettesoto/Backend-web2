import os, shutil
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

router = APIRouter(
    prefix="/uploadImages",
    tags=["Guardar Imagenes"],
    responses={404: {"description": "Not found"}}
)

paciente = 'paciente1'
path = os.path.join('G:', 'Mi unidad', 'pruebasAgendado', paciente, 'img')

# Ruta al archivo de credenciales JSON
credentials_path = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/drive.file']

creds = None
token_path = 'token_drive.json'

if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(token_path, 'w') as token:
        token.write(creds.to_json())

drive_service = build('drive', 'v3', credentials=creds)

@router.post("/image")
async def image(image: UploadFile = File(...)):
    try:
        destination = os.path.join(path, image.filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        with open(destination, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        file_metadata = {'name': image.filename}
        media = MediaFileUpload(destination, mimetype='image/jpeg')
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return JSONResponse(content={"filename": image.filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
