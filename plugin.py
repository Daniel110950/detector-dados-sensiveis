from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import scanner

app = FastAPI()

ALLOWED_EXT = {".txt", ".log", ".csv", ".md", ".json"}
MAX_BYTES = 2 * 1024 * 1024  # 2MB por arquivo (simples e seguro)

@app.get("/", response_class=HTMLResponse)
def tela_upload():
    return Path("templates/upload.html").read_text(encoding="utf-8")

@app.post("/upload")
async def upload_arquivos(files: list[UploadFile] = File(...)):
    # UploadFile/File exige python-multipart instalado. [1](https://fastapi.tiangolo.com/tutorial/request-files/)
    results = []

    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext not in ALLOWED_EXT:
            raise HTTPException(
                status_code=415,
                detail=f"Tipo não suportado: {ext}. Aceitos: {', '.join(sorted(ALLOWED_EXT))}"
            )

        content = await f.read()
        if len(content) > MAX_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande: {f.filename}. Limite: {MAX_BYTES} bytes."
            )

        # Tenta decodificar como texto
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="ignore")

        achados = scanner.detectar(text)  # já mascarado pelo scanner

        results.append({
            "filename": f.filename,
            "achados": achados
        })

    return {"count": len(results), "results": results}