from fastapi import FastAPI

app = FastAPI(title="SIGECORE API")

@app.get("/")
def root():
    return {"mensaje": "Hola SIGECORE"}

@app.get("/health")
def health():
    return {"status": "ok"}