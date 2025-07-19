from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/upload")
def upload_document(file: UploadFile):
    print(file.filename)
