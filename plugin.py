from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import scanner
from fastapi.responses import StreamingResponse
import io, json, csv

ULTIMO_RESULTADO = []
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
    global ULTIMO_RESULTADO
    ULTIMO_RESULTADO = results

    return {"count": len(results), "results": results}

@app.get("/download")
def download(format: str = "json"):
    if not ULTIMO_RESULTADO:
        raise HTTPException(status_code=400, detail="Nenhum relatório disponível")

    if format == "json":
        data = json.dumps(ULTIMO_RESULTADO, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.StringIO(data),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=relatorio.json"}
        )

    if format == "txt":
        out = io.StringIO()
        for f in ULTIMO_RESULTADO:
            out.write(f"Arquivo: {f['filename']}\n")
            for tipo, itens in f["achados"].items():
                out.write(f"  {tipo}:\n")
                for i in itens:
                    out.write(f"    - {i}\n")
            out.write("\n")

        return StreamingResponse(
            io.StringIO(out.getvalue()),
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=relatorio.txt"}
        )

    if format == "csv":
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["arquivo", "tipo", "valor_mascarado"])

        for f in ULTIMO_RESULTADO:
            for tipo, itens in f["achados"].items():
                for i in itens:
                    writer.writerow([f["filename"], tipo, i])

        return StreamingResponse(
            io.StringIO(out.getvalue()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=relatorio.csv"}
        )

    raise HTTPException(status_code=400, detail="Formato inválido")