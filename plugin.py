from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path
import scanner  # usa seu scanner.py

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def tela_upload():
    return Path("templates/upload.html").read_text(encoding="utf-8")

@app.post("/upload")
async def upload_arquivo(file: UploadFile = File(...)):
    caminho = UPLOAD_DIR / file.filename

    conteudo = await file.read()
    caminho.write_bytes(conteudo)

    texto = scanner.ler_arquivo(caminho)
    achados = scanner.detectar(texto)

    return {
        "arquivo": file.filename,
        "achados": achados
    }