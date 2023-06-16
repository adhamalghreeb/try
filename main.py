import io
import os
import json
from fastapi import File,FastAPI, UploadFile
import aiofiles
import whisper

model_wis = whisper.load_model("base")

absolute_path = os.path.dirname(__file__)
relative_path = "static/"
full_path = os.path.join(absolute_path, relative_path)

app = FastAPI()

@app.get("/")
async def root():
    return {"this adham alghreeb, i have spoken"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/voicerecog/")
async def create_upload_file(file: UploadFile = File(...)):
    destination_file_path = full_path+file.filename # location to store file
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read file chunk
            await out_file.write(content)  # async write file chunk
    var_name = full_path+file.filename # path to the uploaded file
    result = model_wis.transcribe(var_name)
    return {'results': result}